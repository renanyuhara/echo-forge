"""Generate an A/B listening benchmark using synthetic preset voices only.

No voice samples, cloning, or third-party hosted inference.
"""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

def commands(python: str, script: str, text_file: str, output_dir: str, speakers: list[str]) -> list[list[str]]:
    return [[python, script, "--speaker", speaker, "--dtype", "float32",
             "--text-file", text_file, "--output", str(Path(output_dir) / f"ptbr-{speaker}.wav")]
            for speaker in speakers]

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Blind-style A/B baseline for original synthetic pt-BR voices")
    p.add_argument("--text-file", default="examples/orfina-voicedesign-short.txt")
    p.add_argument("--output-dir", default="outputs/ptbr-benchmark")
    p.add_argument("--speakers", nargs="+", default=["serena", "vivian"])
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)
    if not Path(args.text_file).is_file():
        p.error(f"Missing text file: {args.text_file}")
    if not args.speakers or any(not s.replace("_", "").isalnum() for s in args.speakers):
        p.error("Speakers must contain only alphanumeric characters or underscores")
    runs = commands(sys.executable, "poc/generate.py", args.text_file, args.output_dir, args.speakers)
    for command in runs:
        print("Running:", " ".join(command), flush=True)
        if not args.dry_run:
            result = subprocess.run(command, check=False)
            if result.returncode:
                print(f"Generation failed with exit code {result.returncode}; stopping.", file=sys.stderr)
                return result.returncode
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
