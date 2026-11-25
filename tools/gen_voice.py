#!/usr/bin/env python3
"""Generate voice clips for a lesson with Kokoro TTS.

Reads tools/<lesson>/lines.json (key -> sentence) and voices.json (first letter
of the key -> voice), writes <lesson>/a/<key>.mp3.

Usage:
  python3 tools/gen_voice.py day-night            # only clips that are missing
  python3 tools/gen_voice.py day-night n_m1 a_hi  # these keys, overwrite
  python3 tools/gen_voice.py day-night --all      # every clip, overwrite

Setup (once per machine; the model files are large, never commit them):
  pip install kokoro-onnx soundfile        # ffmpeg must be on PATH
  curl -L -o /tmp/kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.fp16.onnx
  curl -L -o /tmp/voices.bin  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
Set KOKORO_MODEL / KOKORO_VOICES if the files are somewhere else.
"""
import json, os, pathlib, subprocess, sys, tempfile

import soundfile as sf
from kokoro_onnx import Kokoro

root = pathlib.Path(__file__).resolve().parent.parent
lesson, args = sys.argv[1], sys.argv[2:]
src = root / "tools" / lesson
lines = json.loads((src / "lines.json").read_text(encoding="utf-8"))
voices = json.loads((src / "voices.json").read_text(encoding="utf-8"))
out = root / lesson / "a"
out.mkdir(parents=True, exist_ok=True)

if "--all" in args:
    keys = list(lines)
elif args:
    keys = args
else:
    keys = [k for k in lines if not (out / f"{k}.mp3").exists()]

k = Kokoro(os.environ.get("KOKORO_MODEL", "/tmp/kokoro.onnx"), os.environ.get("KOKORO_VOICES", "/tmp/voices.bin"))
for key in keys:
    v = voices[key[0]]
    samples, rate = k.create(lines[key], voice=v["voice"], speed=v["speed"], lang=v["lang"])
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        sf.write(tmp.name, samples, rate)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp.name, "-ac", "1", "-b:a", "56k", str(out / f"{key}.mp3")], check=True)
    print("voiced", key)
print(len(keys), "clip(s)")
