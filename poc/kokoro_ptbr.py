"""Standalone synthetic pt-BR preset voice test with Kokoro 82M."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Generate Brazilian Portuguese with original synthetic Kokoro voice")
    p.add_argument("--text-file", type=Path, default=Path("examples/orfina-voicedesign-short.txt"))
    p.add_argument("--voice", default="pf_dora", choices=["pf_dora"])
    p.add_argument("--output", type=Path, default=Path("outputs/kokoro-orfina-dora.wav"))
    p.add_argument("--device", choices=["cuda", "cpu"], default="cuda")
    p.add_argument("--speed", type=float, default=1.0)
    return p.parse_args(argv)

def main(argv=None):
    args = parse_args(argv)
    if args.speed <= 0:
        raise SystemExit("--speed must be greater than 0")
    text = args.text_file.read_text(encoding="utf-8-sig").strip()
    if not text:
        raise SystemExit("The source text file is empty.")
    import numpy as np
    import soundfile as sf
    import torch
    from kokoro import KPipeline
    if args.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("CUDA unavailable; pass --device cpu or check drivers.")
    print(f"Loading Kokoro pt-BR female voice {args.voice} on {args.device}", flush=True)
    if args.device == "cuda":
        torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    pipeline = KPipeline(lang_code="p", device=args.device)
    chunks = []
    for result in pipeline(text, voice=args.voice, speed=args.speed):
        chunks.append(result.audio.detach().cpu().numpy())
    if not chunks:
        raise SystemExit("Kokoro returned no audio.")
    audio = np.concatenate(chunks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sf.write(args.output, audio, 24000)
    print(json.dumps({
        "engine": "kokoro-82m",
        "voice": args.voice,
        "language": "pt-BR",
        "device": args.device,
        "generation_seconds": round(time.perf_counter() - started, 2),
        "audio_seconds": round(len(audio) / 24000, 2),
        "peak_gpu_memory_mib": round(torch.cuda.max_memory_allocated() / 2**20, 1) if args.device == "cuda" else None,
        "output": str(args.output),
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
