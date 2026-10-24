#!/usr/bin/env python3
"""
Build-a-Voice — design a custom AI voice character using the local Kokoro
TTS model already on this PC, then have it read back whatever you type.

The model files (kokoro-v0_19.onnx + voices.bin, ~330MB) live at
B:\\AI Directories_Databases\\models\\kokoro, with a leftover fallback
at C:\\Users\\<you>\\kokoro_models if Drive B is unplugged.

Kokoro ships 11 base voices (American/British, female/male). You can use
one as-is, or blend two or more together at custom ratios to make a voice
nobody else has, and save that blend as a named "persona" so you don't have
to re-type the recipe next time.

Usage:
    python speak.py --list-voices
    python speak.py --voice am_adam --text "Hello there." --out hello.wav
    python speak.py --blend "af_bella:0.6,am_adam:0.4" --text "..." --out mix.wav
    python speak.py --blend "af_bella:0.6,am_adam:0.4" --save-persona noir_detective --text "..." --out test.wav
    python speak.py --persona noir_detective --text "Another line." --out line2.wav
    python speak.py --list-personas
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

VOICE_INFO = {
    "af":          "American, feminine — the default/neutral blend",
    "af_bella":    "American, feminine",
    "af_nicole":   "American, feminine",
    "af_sarah":    "American, feminine",
    "af_sky":      "American, feminine",
    "am_adam":     "American, masculine",
    "am_michael":  "American, masculine",
    "bf_emma":     "British, feminine",
    "bf_isabella": "British, feminine",
    "bm_george":   "British, masculine",
    "bm_lewis":    "British, masculine",
}

PERSONAS_DIR = Path(__file__).resolve().parent.parent / "personas"


def find_model_files():
    bases = [
        Path(r"B:\AI Directories_Databases\models\kokoro"),
        Path(r"C:\Users\<you>\kokoro_models"),
    ]
    for base in bases:
        model = base / "kokoro-v0_19.onnx"
        voices = base / "voices.bin"
        if model.is_file() and voices.is_file():
            return model, voices
    return None, None


def load_kokoro():
    try:
        from kokoro_onnx import Kokoro
    except ImportError:
        print(json.dumps({"error": "kokoro-onnx isn't installed. Run: pip install kokoro-onnx"}))
        sys.exit(1)
    model, voices = find_model_files()
    if model is None:
        print(json.dumps({"error": "couldn't find kokoro-v0_19.onnx / voices.bin in B:\\AI Directories_Databases\\models\\kokoro"}))
        sys.exit(1)
    return Kokoro(str(model), str(voices))


def parse_blend(spec, k):
    """'af_bella:0.6,am_adam:0.4' -> (normalized weighted style ndarray, recipe dict)"""
    parts = [p.strip() for p in spec.split(",") if p.strip()]
    recipe = {}
    for p in parts:
        if ":" in p:
            name, weight = p.split(":", 1)
            recipe[name.strip()] = float(weight)
        else:
            recipe[p.strip()] = 1.0
    unknown = [n for n in recipe if n not in VOICE_INFO]
    if unknown:
        raise ValueError(f"unknown voice(s): {', '.join(unknown)}. Run --list-voices to see options.")
    total = sum(recipe.values()) or 1.0
    recipe = {n: w / total for n, w in recipe.items()}
    style = None
    for name, weight in recipe.items():
        v = k.get_voice_style(name) * weight
        style = v if style is None else style + v
    return style.astype(np.float32), recipe


def save_persona(name, recipe, style):
    PERSONAS_DIR.mkdir(parents=True, exist_ok=True)
    np.save(PERSONAS_DIR / f"{name}.npy", style)
    manifest_path = PERSONAS_DIR / "personas.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.is_file() else {}
    manifest[name] = {"recipe": recipe}
    manifest_path.write_text(json.dumps(manifest, indent=2))


def load_persona(name):
    style_path = PERSONAS_DIR / f"{name}.npy"
    if not style_path.is_file():
        raise ValueError(f"no saved persona named '{name}'. Run --list-personas to see what's saved.")
    return np.load(style_path)


def list_personas():
    manifest_path = PERSONAS_DIR / "personas.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.is_file() else {}
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-voices", action="store_true")
    ap.add_argument("--list-personas", action="store_true")
    ap.add_argument("--voice", default=None, help="a single base voice name, e.g. am_adam")
    ap.add_argument("--blend", default=None, help='e.g. "af_bella:0.6,am_adam:0.4"')
    ap.add_argument("--persona", default=None, help="load a previously saved persona by name")
    ap.add_argument("--save-persona", default=None, help="save the resulting --blend as a named persona")
    ap.add_argument("--text", default=None)
    ap.add_argument("--text-file", default=None)
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--lang", default="en-us")
    ap.add_argument("--out", default=None, help="output .wav path")
    args = ap.parse_args()

    if args.list_voices:
        print(json.dumps(VOICE_INFO, indent=2))
        return

    if args.list_personas:
        print(json.dumps(list_personas(), indent=2))
        return

    if not args.out:
        print(json.dumps({"error": "--out is required (a .wav path)"}))
        sys.exit(1)

    text = args.text
    if args.text_file:
        text = Path(args.text_file).read_text(encoding="utf-8")
    if not text:
        print(json.dumps({"error": "provide --text or --text-file"}))
        sys.exit(1)

    k = load_kokoro()

    recipe_used = None
    if args.persona:
        style = load_persona(args.persona)
        voice_arg = style
    elif args.blend:
        style, recipe_used = parse_blend(args.blend, k)
        voice_arg = style
        if args.save_persona:
            save_persona(args.save_persona, recipe_used, style)
    elif args.voice:
        if args.voice not in VOICE_INFO:
            print(json.dumps({"error": f"unknown voice '{args.voice}'. Run --list-voices."}))
            sys.exit(1)
        voice_arg = args.voice
    else:
        print(json.dumps({"error": "provide one of --voice, --blend, or --persona"}))
        sys.exit(1)

    import soundfile as sf
    samples, sr = k.create(text, voice=voice_arg, speed=args.speed, lang=args.lang)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out_path), samples, sr)

    result = {"out": str(out_path), "seconds": round(len(samples) / sr, 2)}
    if recipe_used:
        result["recipe"] = recipe_used
        if args.save_persona:
            result["saved_persona"] = args.save_persona
    elif args.persona:
        result["persona"] = args.persona
    else:
        result["voice"] = args.voice
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
