# Deploy — one authentication step, then live

The site is fully built and committed. `docs/` contains the complete 59-page
static site; GitHub Pages serves it directly from the repo. Nothing needs to
be built on a server.

## Path A — GitHub Pages with gh CLI (recommended, ~60 seconds)

Target: `https://nexuskw.github.io/` (org `nexuskw`,
repo `asu`). Any account/repo works — the site is base-path independent.

```bash
brew install gh                # if not installed
gh auth login                  # one-time browser login (nexuskw org owner)
cd "/Users/ilmshri/Social Media/sun-devil-factory"
gh repo create asu --public --source=. --push
gh api "repos/{owner}/nexuskw.github.io/pages" -X POST \
  -f "source[branch]=main" -f "source[path]=/docs"
```

Live URL: `https://nexuskw.github.io/`
(first build takes a minute or two).

## Path B — GitHub web UI (no CLI)

1. Create an empty **public** repo named `sun-devil-factory` at github.com/new
   (no README).
2. ```bash
   cd "/Users/ilmshri/Social Media/sun-devil-factory"
   git remote add origin https://github.com/<your-username>/sun-devil-factory.git
   git push -u origin main
   ```
3. Repo → Settings → Pages → Source: **Deploy from a branch** →
   Branch `main`, folder `/docs` → Save.

## Path C — Cloudflare Pages (alternative free host)

Dashboard → Workers & Pages → Create → Pages → Upload assets → drag the
`docs/` folder. Or connect the GitHub repo (build command: `python3 build.py`,
output directory: `docs`).

## After any content change

```bash
python3 build.py && git add -A && git commit -m "…" && git push
```

Pages redeploys automatically on push.
