"""Compare two built-in synthetic female voices across three original vows scenes.

No voice cloning, no speaker reference recordings, and no changes to other environments.
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

SCENES = (
    ("01-opening", "examples/orfina-vows-opening.txt", 1.08),
    ("02-intimate", "examples/orfina-vows-intimate.txt", 1.03),
    ("03-finale", "examples/orfina-vows-finale.txt", 0.98),
)
VOICES = ("F1", "F5")


def plan(output_dir: Path, voices=VOICES):
    return [
        (voice, name, Path(source), speed, output_dir / voice.lower() / f"{name}.wav")
        for voice in voices
        for name, source, speed in SCENES
    ]


def main(argv=None):
    p = argparse.ArgumentParser(description="Six WAVs: F1 and F5 in three vows scenes")
    p.add_argument("--output-dir", type=Path, default=Path("outputs/supertonic-vows"))
    p.add_argument("--voices", nargs="+", choices=VOICES, default=list(VOICES))
    p.add_argument("--steps", type=int, default=8)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)
    if not 2 <= args.steps <= 12:
        p.error("--steps must be between 2 and 12")
    jobs = plan(args.output_dir, args.voices)
    for voice, name, source, speed, output in jobs:
        if not source.is_file():
            p.error(f"Missing text: {source}")
        if not source.read_text(encoding="utf-8-sig").strip():
            p.error(f"Empty text: {source}")
        print(f"{voice} / {name} / speed={speed} -> {output}", flush=True)
    if args.dry_run:
        return 0

    from supertonic import TTS
    tts = TTS(auto_download=True)
    styles = {voice: tts.get_voice_style(voice_name=voice) for voice in args.voices}
    for voice, name, source, speed, output in jobs:
        text = source.read_text(encoding="utf-8-sig").strip()
        start = time.perf_counter()
        wav, _duration = tts.synthesize(
            text=text, voice_style=styles[voice], lang="pt",
            speed=speed, total_steps=args.steps
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        tts.save_audio(wav, str(output))
        print(f"Saved {output} in {time.perf_counter() - start:.2f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
