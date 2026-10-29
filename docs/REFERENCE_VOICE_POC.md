# PR #4 — Brazilian Portuguese reference-voice cloning

**Status: experimental, not yet hardware-tested.** The previous Windows CustomVoice 0.6B FP32 model ran on an RTX 2080 SUPER. The Base 0.6B clone workflow is a **different model** and needs its own hardware and listening test.

## Goal

Generate short Orfina lines from a clean, **authorized** Brazilian Portuguese female voice reference. Judge accent, emotional warmth, naturalness, and fidelity. This does **not** copy the voices of professional actors or authorize scraping their recordings. Artist performances may inspire original direction, not unlicensed voice cloning.

The official [Qwen3-TTS 0.6B Base model](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base) supports reference audio + exact transcript via `generate_voice_clone`. This is distinct from VoiceDesign and CustomVoice.

## Obtain a lawful reference

Have an adult volunteer record **5–15 seconds of clean Brazilian Portuguese**, with explicit permission to create a synthetic voice for tabletop RPG use, or obtain a synthetic reference with a license that explicitly allows voice cloning. The speaker should use the warmth and mature feminine style desired for Orfina. A recording with no overlapping speech or background music works best.

Save the recording locally as `references/orfina-consented.wav`. Provide its **exact spoken words** in `references/orfina-reference.txt`. Keep the recording, transcript and output private; they are excluded from Git. Do not assume that permission to listen to content also grants permission to clone its speaker.

## Windows 11 PowerShell

From the repository root on branch `feat/ptbr-reference-voice-clone-poc`:

```powershell
git pull
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Existing dependencies from PR #2 (`torch`, `qwen-tts`, `soundfile`) are reused. **Do not upgrade all packages**: this environment has a validated PyTorch/CUDA configuration and a previously resolved `huggingface_hub` version constraint.

When an authorized audio file and transcript are available:

```powershell
.\.venv\Scripts\python.exe poc/clone_voice.py `
  --reference references/orfina-consented.wav `
  --reference-text-file references/orfina-reference.txt `
  --text-file examples/orfina-voicedesign-short.txt `
  --output outputs/orfina-reference-qwen.wav `
  --dtype float32 `
  --consent
```

The first run may download the 0.6B Base checkpoint, separate from the existing CustomVoice and GGUF models. FP32 + SDPA avoids the FP16 predictor assertion seen earlier on Turing, but **VRAM fit and speed are not yet confirmed for the Base path**. Monitor usage with `nvidia-smi -l 1` in a second terminal. If out of memory, stop and report the error before changing precision.

The script deliberately avoids `x_vector_only_mode` for the first evaluation: the full reference + exact transcript is our quality baseline. The reference and its transcript are processed locally after checkpoint download.

## Evaluation and acceptance

Record whether the model generated a valid WAV; GPU peak allocated memory; generation time; and subjective ratings of native pt-BR pronunciation, lack of robotic artifacts, emotional expression, and resemblance to the *authorized* reference. The objective is to create an **original Orfina voice profile** with consistent future takes; this test only assesses viability. Emotion progression and persistent reference profiles are later work.

**No actual target-GPU cloning success is claimed by this PR until manually verified.**
