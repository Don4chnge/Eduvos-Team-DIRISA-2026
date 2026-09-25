# Hung Council Watch dashboard: source code

Live site: https://eduvos-hung-councils.netlify.app

## Folder contents

| Path | What it is | Edit it? |
|---|---|---|
| `src/template.html` | All the page code: layout (HTML), styling (CSS) and behaviour (JavaScript) | **Yes, make your edits here** |
| `data/data.json` | Forecast, history and model numbers for all 213 municipalities, exported from the ML notebook | Only if the notebook results change |
| `data/geo.json` | Municipal and provincial boundaries (Municipal Demarcation Board) | No |
| `vendor/d3.min.js` | D3.js charting library, bundled so the site works offline | No |
| `build_dashboard.py` | Combines everything into one file | No |
| `dist/index.html` | The finished dashboard, created by the build (not committed to GitHub) | No, it is overwritten by every build |

## How to edit and publish

1. Edit `src/template.html` in VS Code (or any text editor).
2. Build: open a terminal in this folder and run `python build_dashboard.py`.
3. Test: double-click `dist/index.html` to open it in a browser, then copy it to `docs/index.html` in the project folder so the repository stays up to date.
4. Publish: Netlify → project **eduvos-hung-councils** → **Deploys** → drag the `dist` folder into the upload box. The link stays the same.

## Where things are in `src/template.html`

- **Colours and fonts:** the `:root` blocks at the top of `<style>`. There are three colour blocks (light, dark by system setting, dark by toggle); change a colour in all three.
- **Page text and tabs:** the HTML between `<body>` and `<footer>`, one `<section>` per tab (`v-forecast`, `v-trends`, `v-model`, `v-data`).
- **Party colours:** `var PARTY = {...}` near the start of the script.
- **Risk calculation:** `function risk(m, s)`. It uses the model coefficients `DATA.model.b0` and `DATA.model.b1` from the ML notebook; do not change the formula, or the dashboard will no longer match the model.
- **Swing presets:** the buttons with `data-swing="..."` in the swing panel.

## Rules to keep it working

- Do not delete the placeholders `__DATA__` and `__GEO__`, or the D3 `<script src=...>` line; the build script replaces them.
- Keep every number shown in the dashboard consistent with the notebooks and slides.
- After any edit, check the page in both dark and light mode (button in the top-right corner) and on a phone.
