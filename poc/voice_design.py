"""Run Qwen3-TTS VoiceDesign GGUF through a Linux CUDA Docker container.

Weights, text, and output remain local; no hosted inference is used.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

IMAGE = "ghcr.io/serveurpersocom/qwentts.cpp:cuda12"
VOICE_INSTRUCTION = (
    "A gentle, warm female voice speaking Brazilian Portuguese (pt-BR), "
    "with a soft intimate tone, natural Brazilian pronunciation, "
    "delicate articulation, affectionate delivery and subtle emotion. "
    "Avoid robotic delivery and foreign-accented pronunciation."
)
MODEL_NAMES = {
    "q8": ("qwen-talker-1.7b-voicedesign-Q8_0.gguf", "qwen-tokenizer-12hz-Q8_0.gguf"),
    "q4": ("qwen-talker-1.7b-voicedesign-Q4_K_M.gguf", "qwen-tokenizer-12hz-Q4_K_M.gguf"),
}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Local GGUF VoiceDesign test via Docker + NVIDIA GPU")
    p.add_argument("--models-dir", type=Path, default=Path("models"))
    p.add_argument("--quant", choices=tuple(MODEL_NAMES), default="q8")
    p.add_argument("--text-file", type=Path, default=Path("examples/orfina-vows.txt"))
    p.add_argument("--output", type=Path, default=Path("outputs/orfina-voicedesign-q8.wav"))
    p.add_argument("--instruct", default=VOICE_INSTRUCTION)
    p.add_argument("--lang", default="Portuguese")
    p.add_argument("--image", default=IMAGE, help="Locally trusted GGML CUDA image")
    p.add_argument("--dry-run", action="store_true", help="Print configuration; do not run Docker")
    return p


def docker_command(args: argparse.Namespace) -> tuple[list[str], str, Path]:
    model_dir = args.models_dir.resolve()
    talker_name, codec_name = MODEL_NAMES[args.quant]
    missing = [name for name in (talker_name, codec_name) if not (model_dir / name).is_file()]
    if missing and not args.dry_run:
        raise ValueError("Required GGUF model files are missing in " + str(model_dir) + ": " + ", ".join(missing))
    if not args.text_file.is_file():
        raise ValueError(f"Text file does not exist: {args.text_file}")
    script = args.text_file.read_text(encoding="utf-8-sig").strip()
    if not script:
        raise ValueError("Text file is empty")
    if not args.instruct.strip():
        raise ValueError("VoiceDesign requires a nonempty --instruct description")
    output = args.output.resolve()
    if not args.dry_run:
        output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "docker", "run", "--rm", "--gpus", "all", "-i",
        "--network", "none",
        "--mount", f"type=bind,source={model_dir},target=/models,readonly",
        "--mount", f"type=bind,source={output.parent},target=/output",
        "--entrypoint", "/app/qwen-tts", args.image,
        "--model", f"/models/{talker_name}",
        "--codec", f"/models/{codec_name}",
        "--device", "CUDA0", "--lang", args.lang,
        "--instruct", args.instruct,
        "-o", f"/output/{output.name}",
    ]
    return cmd, script, output


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        cmd, script, output = docker_command(args)
    except (OSError, ValueError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2
    if args.dry_run:
        print(json.dumps({"docker_argv": cmd, "script": script, "output": str(output)}, indent=2, ensure_ascii=False))
        return 0
    print(f"Generating with {args.quant.upper()} quantization on CUDA0; writing {output}", flush=True)
    try:
        process = subprocess.run(cmd, input=script, text=True, encoding="utf-8", check=False)
    except FileNotFoundError:
        print("Docker CLI not found. Start Docker Desktop and confirm 'docker version'.", file=sys.stderr)
        return 2
    if process.returncode != 0:
        print(f"Docker/inference failed (exit {process.returncode}). Check GPU access and model paths.", file=sys.stderr)
        return process.returncode
    if not output.is_file() or output.stat().st_size == 0:
        print("Inference reported success, but the WAV output was not found or is empty.", file=sys.stderr)
        return 1
    print(f"WAV generated: {output} ({output.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
