# Design-session tooling (2026-07-31)

- gen_logos.py + outline.py — logo candidates: harfbuzz-shaped, outlined
  Source Serif 4 / IBM Plex Sans Arabic (both SIL OFL 1.1; download TTFs
  from google/fonts into a local fonts/ dir — not committed).
- capture_motion3.py — records the motion-tree journeys as GIFs. Playwright
  MUST attach to a manually-launched Chrome (connect_over_cdp): Playwright's
  own launcher passes --disable-features=PaintHolding, which silently kills
  cross-document view transitions. Python urllib also fails TLS on this
  machine (trust store) — shell out to curl for any web fetch.
- build_gallery.py — assembles the self-contained review-gallery artifact.
