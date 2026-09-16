# AGENTS.md

## Cursor Cloud specific instructions

This repo is a **static front-end page** ("Visitor File Submissions" intake form). There is
**no package manager, no build step, no tests, and no lint config** — it is plain HTML/CSS.
Nothing needs to be installed; the update script is intentionally a no-op. `python3` is
preinstalled and is all you need to serve the site.

### Running the site (dev)
- Serve the repo with any static server, e.g. `python3 -m http.server 8000` from the repo root,
  then open `http://localhost:8000/`. There is no hot-reload; refresh the browser after edits.

### Important gotcha: the files are mislabeled
The committed filenames do **not** match their contents:
- `index.html` is actually a **PNG image** (byte-identical to `assets/culinary-review.png`).
- `script.js` actually contains the **HTML document** for the page.
- `styles.css` is the only correctly-named file (real CSS).

Consequences:
- Opening `http://localhost:8000/` (i.e. `index.html`) serves the **PNG**, not the form.
- The HTML references `<script src="script.js">`, but `script.js` is HTML, so the intended
  interactive behavior (drag-drop upload, completion meter, generated receipt, receipt history)
  has **no working JavaScript** in the current tree. Native HTML inputs (typing, selects,
  checkbox) still work without JS.

To render/preview the *intended* page without changing the repo, copy the files into a scratch
dir with corrected names, e.g.:
```
mkdir -p /tmp/render/assets
cp script.js /tmp/render/index.html
cp styles.css /tmp/render/styles.css
cp assets/culinary-review.png /tmp/render/assets/
python3 -m http.server 8001   # run from /tmp/render, open http://localhost:8001/
```
Do not "fix" the filenames in the repo as part of unrelated tasks — treat it as intentional
unless the user explicitly asks to correct it.
