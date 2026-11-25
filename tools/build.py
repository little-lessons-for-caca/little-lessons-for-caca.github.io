#!/usr/bin/env python3
"""Build a lesson page: tools/<lesson>/template.html + lines.json -> <lesson>/index.html

Usage: python3 tools/build.py day-night
"""
import json, pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
lesson = sys.argv[1]
src = root / "tools" / lesson
lines = json.loads((src / "lines.json").read_text(encoding="utf-8"))
html = (src / "template.html").read_text(encoding="utf-8").replace("__LINES__", json.dumps(lines))
out = root / lesson / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf-8")
print("wrote", out.relative_to(root), len(lines), "lines")
