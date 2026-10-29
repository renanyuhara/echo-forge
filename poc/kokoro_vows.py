"""Produce three independent Orfina speech takes using the established Kokoro preset."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PARTS = (
    ("opening", "examples/orfina-vows-opening.txt", 1.08),
    ("intimate", "examples/orfina-vows-intimate.txt", 1.03),
    ("finale", "examples/orfina-vows-finale.txt", 0.98),
)


def build_commands(python=sys.executable, output_dir="outputs/orfina-vows", device="cuda"):
    return [
        [python, "poc/kokoro_ptbr.py", "--text-file", source, "--output",
         str(Path(output_dir) / f"{index:02d}-{name}.wav"), "--voice", "pf_dora",
         "--speed", str(speed), "--device", device]
        for index, (name, source, speed) in enumerate(PARTS, 1)
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Three-step original Orfina voice experiment")
    parser.add_argument("--output-dir", default="outputs/orfina-vows")
    parser.add_argument("--device", choices=("cuda", "cpu"), default="cuda")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    commands = build_commands(output_dir=args.output_dir, device=args.device)
    for command in commands:
        print(" ".join(command), flush=True)
        if not args.dry_run:
            if not Path(command[command.index("--text-file") + 1]).is_file():
                parser.error("Missing example text file")
            result = subprocess.run(command, check=False)
            if result.returncode:
                return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
