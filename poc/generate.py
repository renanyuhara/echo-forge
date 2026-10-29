"""Local Qwen3-TTS text-to-WAV feasibility spike. No hosted inference calls."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


DEFAULT_MODEL = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"
DEFAULT_TEXT = "Astel, mesmo quando os caminhos nos separaram, meu coração sempre encontrou o caminho de volta para você."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a local Portuguese WAV with Qwen3-TTS.")
    parser.add_argument("--text", default=DEFAULT_TEXT, help="Text to speak (default: sample line).")
    parser.add_argument("--text-file", type=Path, help="UTF-8 file containing the dialogue.")
    parser.add_argument("--output", type=Path, default=Path("outputs/orfina-test.wav"))
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model identifier or local checkpoint directory.")
    parser.add_argument("--speaker", help="Speaker supported by the model; use --list-speakers to inspect.")
    parser.add_argument("--list-speakers", action="store_true")
    parser.add_argument("--language", default="Portuguese", help="Model language, not an accent guarantee.")
    parser.add_argument("--instruct", help="Optional delivery instruction (model support varies).")
    parser.add_argument("--device", choices=["cuda", "cpu"], default="cuda")
    parser.add_argument("--allow-cpu", action="store_true", help="Explicitly allow slower CPU processing.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.device == "cpu" and not args.allow_cpu:
        raise SystemExit("CPU execution is opt-in. Use --device cpu --allow-cpu.")
    import torch
    import soundfile as sf
    from qwen_tts import Qwen3TTSModel

    if args.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("CUDA not detected. Run 'python poc/diagnose.py' and verify WSL2 drivers/PyTorch.")
    if args.text_file:
        text = args.text_file.read_text(encoding="utf-8").strip()
    else:
        text = args.text.strip()
    if not text and not args.list_speakers:
        raise SystemExit("No text provided.")

    dtype = torch.float16 if args.device == "cuda" else torch.float32
    print(f"Loading {args.model} on {args.device} (dtype={dtype}); first run may download weights.")
    model = Qwen3TTSModel.from_pretrained(
        args.model,
        device_map="cuda:0" if args.device == "cuda" else "cpu",
        dtype=dtype,
        attn_implementation="sdpa",
    )
    speakers = list(model.get_supported_speakers())
    print("Available speakers:", ", ".join(speakers))
    if args.list_speakers:
        return
    if not speakers:
        raise SystemExit("Model returned no preset speakers; use a CustomVoice checkpoint.")
    speaker = args.speaker or speakers[0]
    if speaker not in speakers:
        raise SystemExit(f"Unknown speaker {speaker!r}. Choose one of: {', '.join(speakers)}")
    if args.device == "cuda":
        torch.cuda.reset_peak_memory_stats()
    start = time.perf_counter()
    kwargs = dict(text=text, language=args.language, speaker=speaker)
    if args.instruct:
        kwargs["instruct"] = args.instruct
    with torch.inference_mode():
        wavs, sample_rate = model.generate_custom_voice(**kwargs)
    elapsed = round(time.perf_counter() - start, 2)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(args.output), wavs[0], sample_rate)
    duration = round(len(wavs[0]) / sample_rate, 2)
    stats = {
        "model": args.model, "speaker": speaker, "language": args.language,
        "device": args.device, "generation_seconds": elapsed,
        "audio_seconds": duration, "sample_rate": sample_rate,
        "peak_gpu_memory_mib": round(torch.cuda.max_memory_allocated() / 2**20, 1) if args.device == "cuda" else None,
        "output": str(args.output),
    }
    print(json.dumps(stats, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
