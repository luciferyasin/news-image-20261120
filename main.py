#!/usr/bin/env python3
"""Entrypoint for the 20 November 2026 news-image entry.

The finished front page lives in entry.png next to this file; the program
only copies it into the output directory, so running it twice writes
byte-identical files.

Run it locally with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

if not os.path.exists(SRC):
    sys.exit("entry.png is missing next to main.py")

# entry.png is a JPEG by magic bytes (the rules allow PNG or JPEG under
# this name); copy it verbatim so the output is byte-identical every run.
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
dst = os.path.join(out_dir, "entry.png")
shutil.copyfile(SRC, dst)
if os.path.getsize(dst) != os.path.getsize(SRC):
    sys.exit("entry.png copy is incomplete")
print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
