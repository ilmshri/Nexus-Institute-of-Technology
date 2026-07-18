# Deploy — Nexus Institute of Technology

The site is a fully static build committed to the repo. GitHub Pages serves the
`docs/` folder of `main` directly — nothing runs on a server.

- **Live URL:** https://nexuskw.github.io/
- **Code home:** `github.com/ilmshri/Nexus-Institute-of-Technology` (origin fetch URL)
- **Live-site repo:** `github.com/nexuskw/nexuskw.github.io` — GitHub Pages serves
  the site from THIS repo (`main`, `/docs`); the Pages URL is bound to its name,
  so it must keep receiving pushes for the site to update
- **Push config:** `origin` carries BOTH push URLs — one `git push origin main`
  updates the code home *and* the live site (credential in the Mac's keychain)

## After any content change

```bash
cd "/Users/ilmshri/Social Media/sun-devil-factory"
python3 nexus_build.py                       # rebuild — must end with the summary lines
git add -A && git commit -m "describe change"
git push origin main                         # live ~1 minute later
```

Always build with `nexus_build.py`. (`build.py` is its import library — deploying
from it emits the retired previous-generation site.)

## Local preview

```bash
python3 -m http.server -d docs 8000    # → http://localhost:8000
```

## Verify after deploy

Open https://nexuskw.github.io/curriculum/ and confirm the coverage counter and
your changed pages. If a push doesn't appear within ~2 minutes, check
repo → Actions for the Pages build status.
