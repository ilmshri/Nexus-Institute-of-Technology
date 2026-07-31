#!/usr/bin/env python3
"""Record MechEd motion journeys: manual Chrome launch + CDP screencast (VT-safe)."""
import asyncio
import base64
import io
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE = "http://localhost:8010/design-previews"
OUT = Path(__file__).parent / "gifs"
OUT.mkdir(exist_ok=True)

JOURNEY = [
    ("goto", "/curriculum/index.html", 900),
    ("click", 'a.course-card[href$="math-1/index.html"]', 3400),
    ("click", 'button[data-tab="ct-reference"]', 1500),
    ("click", 'button[data-tab="ct-syllabus"]', 900),
    ("click", '.syl h4 a[href^="02-"]', 3400),
    ("click", '.prevnext a[href^="03-"]', 3400),
]


async def record(tree, out_name, port, mobile=False, waits_scale=1.0, fps=12):
    prof = tempfile.mkdtemp(prefix="vtrec")
    proc = subprocess.Popen([CHROME, f"--user-data-dir={prof}", "--no-first-run",
        "--no-default-browser-check", f"--remote-debugging-port={port}",
        "--window-position=40,40", "--window-size=1300,860", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2.5)
    frames = []
    try:
        async with async_playwright() as p:
            b = await p.chromium.connect_over_cdp(f"http://localhost:{port}")
            pg = b.contexts[0].pages[0]
            cdp = await b.contexts[0].new_cdp_session(pg)
            if mobile:
                await cdp.send("Emulation.setDeviceMetricsOverride",
                               {"width": 390, "height": 760, "deviceScaleFactor": 2, "mobile": True})

            def on_frame(params):
                frames.append((time.time(), params["data"]))
                asyncio.ensure_future(
                    cdp.send("Page.screencastFrameAck", {"sessionId": params["sessionId"]}))

            cdp.on("Page.screencastFrame", on_frame)
            await cdp.send("Page.startScreencast", {
                "format": "png",
                "maxWidth": 800 if mobile else 1300, "maxHeight": 1600, "everyNthFrame": 1})
            for kind, target, wait in JOURNEY:
                if kind == "goto":
                    await pg.goto(f"{BASE}/{tree}{target}")
                else:
                    await pg.click(target, force=True, timeout=15000)
                await pg.wait_for_timeout(int(wait * waits_scale))
            try:
                await cdp.send("Page.stopScreencast")
            except Exception:
                pass
            await b.close()
    finally:
        proc.terminate()
        proc.wait()
        shutil.rmtree(prof, ignore_errors=True)

    if not frames:
        print(f"{out_name}: NO FRAMES")
        return
    t0, t1 = frames[0][0], frames[-1][0]
    step = 1.0 / fps
    ticks, fi, t = [], 0, t0
    while t <= t1:
        while fi + 1 < len(frames) and frames[fi + 1][0] <= t:
            fi += 1
        ticks.append(fi)
        t += step
    scale_to = 390 if mobile else 720
    step_ms = int(1000 / fps)
    imgs, durs, last_fi = [], [], None
    for fi in ticks:
        if fi == last_fi and durs:
            durs[-1] += step_ms
            continue
        img = Image.open(io.BytesIO(base64.b64decode(frames[fi][1]))).convert("RGB")
        if img.width > scale_to:
            img = img.resize((scale_to, int(img.height * scale_to / img.width)), Image.LANCZOS)
        imgs.append(img.quantize(colors=160, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG))
        durs.append(step_ms)
        last_fi = fi
    path = OUT / out_name
    imgs[0].save(path, save_all=True, append_images=imgs[1:],
                 duration=durs, loop=0, optimize=True)
    print(f"{out_name}: {len(frames)} raw -> {len(imgs)} frames, {path.stat().st_size // 1024} KB")


async def main():
    await record("motion-a-slow", "motion-a-slow-desktop.gif", 9401)
    await record("motion-b-slow", "motion-b-slow-desktop.gif", 9402)
    await record("motion-c-slow", "motion-c-slow-desktop.gif", 9403)
    await record("motion-b", "motion-b-realspeed-desktop.gif", 9404, waits_scale=0.4)
    await record("motion-b-slow", "motion-b-slow-mobile.gif", 9405, mobile=True)

asyncio.run(main())
