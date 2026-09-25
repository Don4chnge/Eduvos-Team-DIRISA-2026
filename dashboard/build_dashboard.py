"""Build the Hung Council Watch dashboard into one self-contained file.

Usage (from this folder):  python build_dashboard.py
Output:                    dist/index.html  (upload the dist folder to Netlify)

The script inserts the data, the map boundaries and the D3 charting library into
src/template.html, so the finished page needs no server and works offline.
"""
from pathlib import Path

HERE = Path(__file__).parent
CDN_TAG = '<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>'

template = (HERE / "src" / "template.html").read_text(encoding="utf-8")
data = (HERE / "data" / "data.json").read_text(encoding="utf-8").replace("</", "<\\/")
geo = (HERE / "data" / "geo.json").read_text(encoding="utf-8")
d3 = (HERE / "vendor" / "d3.min.js").read_text(encoding="utf-8").replace("</script", "<\\/script")

for marker in ("__DATA__", "__GEO__", CDN_TAG):
    assert marker in template, f"Missing {marker!r} in template.html; do not remove it."

page = (template.replace("__DATA__", data)
                .replace("__GEO__", geo)
                .replace(CDN_TAG, "<script>/* d3 v7.8.5, ISC licence, https://d3js.org */\n" + d3 + "\n</script>"))

out = HERE / "dist" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(page, encoding="utf-8")
print(f"Built {out} ({len(page) / 1024:.0f} KB)")
