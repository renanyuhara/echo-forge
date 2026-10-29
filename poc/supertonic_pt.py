"""Compare licensed, built-in Supertonic female preset voices without cloning."""
from __future__ import annotations
import argparse
import time
from pathlib import Path

VOICES = ("F1", "F2", "F3", "F4", "F5")

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Compare original female preset voices in Portuguese")
    p.add_argument("--text-file", type=Path, default=Path("examples/orfina-voicedesign-short.txt"))
    p.add_argument("--output-dir", type=Path, default=Path("outputs/supertonic-pt"))
    p.add_argument("--voices", nargs="+", choices=VOICES, default=list(VOICES))
    p.add_argument("--speed", type=float, default=1.05)
    p.add_argument("--steps", type=int, default=8)
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)

def main(argv=None):
    args = parse_args(argv)
    if not 0.7 <= args.speed <= 2.0:
        raise SystemExit("--speed must be between 0.7 and 2.0")
    if not 2 <= args.steps <= 12:
        raise SystemExit("--steps must be between 2 and 12")
    text = args.text_file.read_text(encoding="utf-8-sig").strip()
    if not text:
        raise SystemExit("Empty input text.")
    for voice in args.voices:
        print(f"{voice}: pt, speed={args.speed}, steps={args.steps} -> {args.output_dir / (voice.lower() + '.wav')}", flush=True)
    if args.dry_run:
        return 0
    from supertonic import TTS
    start = time.perf_counter()
    tts = TTS(auto_download=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for voice in args.voices:
        style = tts.get_voice_style(voice_name=voice)
        run_start = time.perf_counter()
        wav, _duration = tts.synthesize(
            text=text, voice_style=style, lang="pt",
            speed=args.speed, total_steps=args.steps
        )
        output = args.output_dir / f"{voice.lower()}.wav"
        tts.save_audio(wav, str(output))
        print(f"Saved {output}; generation_seconds={time.perf_counter() - run_start:.2f}", flush=True)
    print(f"Completed in {time.perf_counter() - start:.2f} s including initialization.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
