# Original synthetic pt-BR voice benchmark

## Purpose

Find a **natural Brazilian Portuguese voice for Orfina without cloning anyone**. Voice direction: mature, gentle, warm, feminine, fairy-tale grace without childishness, and emotionally expressive in private. Original speaker identity matters more than resemblance to any professional performer.

## Evidence so far

- RTX 2080 SUPER / Windows 11 / CUDA successfully generated Qwen3-TTS 0.6B CustomVoice audio in FP32.
- User listening feedback: `vivian` had better Brazilian pronunciation; `serena` was softer but noticeably foreign-accented.
- Qwen3-TTS VoiceDesign 1.7B GGUF Q8 ran on 8 GB VRAM, but its pt-BR pronunciation was judged unacceptably foreign.
- These findings **do not** show that other models will have good pt-BR or that a voice can be designed freely without reference samples.

## Phase A — reproducible baseline (this PR)

From Windows PowerShell, use the existing .venv without installing or upgrading dependencies:

```powershell
git fetch origin
git switch --track origin/feat/ptbr-voice-benchmark
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe poc/compare_ptbr.py --dry-run
.\.venv\Scripts\python.exe poc/compare_ptbr.py
```

Two locally generated WAVs will be written under `outputs/ptbr-benchmark/` using the same short Portuguese phrase and FP32:
`ptbr-serena.wav` and `ptbr-vivian.wav`. The existing model and download cache are reused.

Listen for Brazilian vowels/rhythm, softness, human expressiveness, and speaker stability. Ideally listen without looking at filenames first, using a simple 1–5 scoring system (5 = best).

| Voice | Native pt-BR (1–5) | Naturalness (1–5) | Warmth (1–5) | Expressiveness (1–5) | Notes |
|---|---|---|---|---|---|
| Serena | | | | | |
| Vivian | | | | | |

## Phase B — alternative original synthetic voices (not implemented yet)

Investigate licensed **predefined pt-BR synthetic voices** and engines that genuinely create a new identity from a text description. They are different capabilities. Possible candidate engines include Kokoro variants distributed with pt-BR voices and Piper pt_BR voice packs, **subject to actual voice/model/license verification**.

Do not represent reference-based cloning engines (e.g., Qwen3-TTS Base, XTTS-v2, F5-TTS, Chatterbox) as no-reference voice design. Do not download or clone performer recordings. Any future candidate must include a documented source, license, hardware check, and a repeatable generation command before we promote it as a working EchoForge engine.

## Acceptance

- Same short text tested across at least two original synthetic voices.
- WAV files stay local (ignored by Git).
- Test results documented, including whether native Brazilian pronunciation is satisfactory.
- No reference audio or imitation workflow.
- Continue to another engine if both baseline speakers fail quality review.

This branch provides a controlled baseline and tests, **not yet a new TTS engine or a finished Orfina voice**.
