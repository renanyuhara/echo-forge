"""Local pt-BR reference cloning spike using Qwen3-TTS 0.6B Base.

Only use a reference voice with permission for synthesis.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


MODEL = "Qwen/Qwen3-TTS-12Hz-0.6B-Base"


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Clone a consented reference voice to pt-BR WAV")
    p.add_argument("--reference", type=Path, required=True, help="Local authorized speech recording (WAV preferred).")
    p.add_argument("--reference-text", help="Exact words spoken in the recording.")
    p.add_argument("--reference-text-file", type=Path, help="UTF-8 transcript of the reference.")
    p.add_argument("--text-file", type=Path, default=Path("examples/orfina-voicedesign-short.txt"))
    p.add_argument("--output", type=Path, default=Path("outputs/orfina-reference-qwen.wav"))
    p.add_argument("--language", default="Portuguese")
    p.add_argument("--model", default=MODEL)
    p.add_argument("--dtype", choices=("float32", "float16", "bfloat16"), default="float32")
    p.add_argument("--device", choices=("cuda", "cpu"), default="cuda")
    p.add_argument("--allow-cpu", action="store_true")
    p.add_argument("--consent", action="store_true", help="Confirm authorization to synthesize this reference voice.")
    return p.parse_args(argv)


def prepare(args):
    if not args.consent:
        raise ValueError("Explicit permission is required: pass --consent for an authorized reference voice.")
    if args.device == "cpu" and not args.allow_cpu:
        raise ValueError("CPU execution requires --allow-cpu.")
    if not args.reference.is_file():
        raise ValueError(f"Reference file not found: {args.reference}")
    transcript = args.reference_text
    if args.reference_text_file:
        if transcript is not None:
            raise ValueError("Use either --reference-text or --reference-text-file, not both.")
        transcript = args.reference_text_file.read_text(encoding="utf-8-sig")
    if not transcript or not transcript.strip():
        raise ValueError("Provide an exact transcript using --reference-text-file or --reference-text.")
    if not args.text_file.is_file():
        raise ValueError(f"Text file not found: {args.text_file}")
    text = args.text_file.read_text(encoding="utf-8-sig").strip()
    if not text:
        raise ValueError("Text file is empty.")
    return text, transcript.strip()


def main(argv=None):
    args = parse_args(argv)
    try:
        text, transcript = prepare(args)
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc

    import torch
    import soundfile as sf
    from qwen_tts import Qwen3TTSModel

    if args.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("CUDA unavailable. Run python poc/diagnose.py first.")
    if args.dtype == "bfloat16" and args.device == "cuda" and not torch.cuda.is_bf16_supported():
        raise SystemExit("GPU does not support native BF16; prefer --dtype float32.")
    if args.dtype == "float16":
        print("WARNING: FP16 previously caused a device-side assert on RTX 2080 SUPER. FP32 recommended.")
    print("Loading the Base model. First execution may download model weights.", flush=True)
    model = Qwen3TTSModel.from_pretrained(
        args.model,
        device_map="cuda:0" if args.device == "cuda" else "cpu",
        dtype=getattr(torch, args.dtype),
        attn_implementation="sdpa",
    )
    if args.device == "cuda":
        torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    with torch.inference_mode():
        wavs, rate = model.generate_voice_clone(
            text=text,
            language=args.language,
            ref_audio=str(args.reference.resolve()),
            ref_text=transcript,
        )
    elapsed = time.perf_counter() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(args.output), wavs[0], rate)
    report = {
        "model": args.model,
        "device": args.device,
        "dtype": args.dtype,
        "language": args.language,
        "generation_seconds": round(elapsed, 2),
        "audio_seconds": round(len(wavs[0]) / rate, 2),
        "peak_gpu_memory_mib": round(torch.cuda.max_memory_allocated() / 2**20, 1) if args.device == "cuda" else None,
        "output": str(args.output),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
