# Local TTS proof of concept

This is **an experimental command-line script, not the EchoForge app**. It uses local model inference after an initial weight download. It does **not** generate a unique Orfina voice yet: the first test uses a preset speaker. The eventual voice-design and reference-cloning workflow is a later milestone.

## Target and limitations

- Windows 11 native PowerShell (primary), NVIDIA RTX 2080 SUPER (8 GiB). WSL2 Ubuntu is optional.
- Python 3.12 recommended by upstream Qwen3-TTS.
- Start with the 0.6B **CustomVoice** checkpoint for preset-voice synthesis.
- The model advertises Portuguese but **Brazilian pronunciation must be judged by listening**.
- Compatibility, memory use, time, and quality on this specific GPU are **not yet measured**.
- Do not install FlashAttention-2: Turing / compute capability 7.5 is not its supported target. The script requests PyTorch SDPA, and uses float16 for CUDA.
- The model may exceed available memory or require compatible PyTorch/transformers versions. Treat a failure as evidence for model selection, not a reason to disable safety checks.

## Setup in Windows 11 PowerShell (preferred)

Install **Python 3.12 (64-bit)** from python.org if `py -3.12 --version` does not work. In PowerShell, from the repo directory:

```powershell
nvidia-smi
py -3.12 --version
py -3.12 -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install --upgrade pip
# IMPORTANT: install the CUDA-enabled PyTorch Windows build from
# https://pytorch.org/get-started/locally/ before the next command.
.\\.venv\\Scripts\\python.exe -m pip install qwen-tts soundfile
.\\.venv\\Scripts\\python.exe poc/diagnose.py
```

A Python virtual environment is isolated from the system installation. Using its executable avoids PowerShell execution-policy issues. The PyTorch installation command depends on supported CUDA wheels and NVIDIA driver. **Check `cuda_available: true`** before downloading weights. Qwen3-TTS's SoX dependency may require extra native Windows setup; troubleshoot based on the actual import/runtime error instead of installing unrelated tools in advance.

## Alternative: WSL2 Ubuntu

Optional for dependency compatibility. Install a real Ubuntu distribution first; the Docker Desktop internal `docker-desktop` WSL distribution is **not** a development Ubuntu environment. Then use a Python 3.12 venv and an appropriate CUDA-enabled PyTorch wheel under Linux.

**Verify** that `cuda_available` is true and GPU is NVIDIA RTX 2080 SUPER before continuing. The actual CUDA PyTorch wheel must match your setup; the command above deliberately avoids pinning an unverified wheel URL.

## Generate

```bash
python poc/generate.py --list-speakers
python poc/generate.py --text "Astel, eu prometo caminhar ao seu lado, mesmo quando o mundo tentar nos separar." --output outputs/orfina-test.wav
```

Or use a text file:

```bash
python poc/generate.py --text-file examples/orfina-vows.txt --output outputs/orfina-test.wav
```

The first generation downloads weights from Hugging Face. Subsequent inference is local. Use `--model /path/to/downloaded/checkpoint` to force a local checkpoint. Keep data offline after models are cached and paths configured.

`--list-speakers` loads the checkpoint and shows its available preset speakers, allowing selection with `--speaker`. Try `--instruct` optionally, but do not assume emotion controls will be honored on the 0.6B preset voice checkpoint.

## Measure and report

Copy the JSON statistics printed after generation and note:
- GPU / CUDA / torch versions, operating system and Python version.
- Success/failure and full diagnostic traceback (remove private paths if needed).
- Peak allocated GPU memory (not total VRAM usage), latency, sample duration.
- Listening results for **pt-BR accent, intelligibility, naturalness and expressiveness**.
- Whether a repeated run sounds similar enough for the intended RPG use.

Avoid uploading character samples or private scripts with an issue. The output and caches should stay local. This is a **spike only**; no claims of target hardware validation are made.

Upstream references:
- https://github.com/QwenLM/Qwen3-TTS
- https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice
