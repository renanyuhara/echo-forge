# VoiceDesign GGUF proof of concept (PR #3)

**Status: experimental.** The Windows/PyTorch 0.6B CustomVoice path has been tested on an RTX 2080 SUPER. **The 1.7B VoiceDesign GGUF path has not yet been executed on this hardware.**

This experiment runs a Linux CUDA container from **Windows 11 PowerShell**, using the third-party [qwentts.cpp](https://github.com/ServeurpersoCom/qwentts.cpp) implementation. It does not modify our working Windows PyTorch environment.

## Why Docker instead of a separate Ubuntu installation?

Docker Desktop on Windows uses WSL2 for Linux containers and supports NVIDIA GPU passthrough via `--gpus all`. A separate Ubuntu distribution is not required. Windows, WSL2 and Docker **share the same physical 8 GiB of VRAM**: changing OS does not expand capacity or grant native BF16 support on Turing. Native Linux could avoid some Windows graphics usage, but is not necessary for this test. Linux tools simplify building the upstream qwentts.cpp engine, and a published image avoids building it ourselves.

References: [Docker GPU support](https://docs.docker.com/desktop/features/gpu/), [Docker WSL2 backend](https://docs.docker.com/desktop/features/wsl/), [NVIDIA CUDA on WSL2](https://docs.nvidia.com/cuda/wsl-user-guide/).

## 1. Verify Docker Desktop

Start Docker Desktop. Confirm **Linux containers** with the **WSL2 backend**. In PowerShell:

```powershell
docker version
docker info --format '{{.OSType}}'
```

The second command should print `linux`. To confirm **GPU access inside** the runtime (Windows PyTorch success does not prove container support):

```powershell
docker run --rm --gpus all --entrypoint nvidia-smi ghcr.io/serveurpersocom/qwentts.cpp:cuda12
```

The first invocation downloads a potentially large third-party image. This image is supplied by the independent qwentts.cpp maintainer, not the Qwen team.

## 2. Download only the two Q8 GGUF files

From `C:\projects\echo-forge`, on the PR #3 branch:

```powershell
.\.venv\Scripts\python.exe -m pip install "huggingface_hub==0.36.2"
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\hf.exe download Serveurperso/Qwen3-TTS-GGUF `
  qwen-talker-1.7b-voicedesign-Q8_0.gguf `
  qwen-tokenizer-12hz-Q8_0.gguf `
  --local-dir models
```

Do not run an unbounded `--upgrade huggingface_hub` in the same environment as Qwen3-TTS: current 2.x releases may conflict with transformers/gradio. If you already upgraded, restore `huggingface_hub==0.36.2` and run `pip check` first.

Files: [Hugging Face model repository](https://huggingface.co/Serveurperso/Qwen3-TTS-GGUF/tree/main). These Q8 files are approximately **2.04 GB + 291 MB on disk**. File size is *not* peak VRAM. Do not download the entire repository. The `models/` directory is Git-ignored.

## 3. Validate command construction

```powershell
.\.venv\Scripts\python.exe poc/voice_design.py --dry-run --text-file examples/orfina-voicedesign-short.txt
```

Dry run does not load weights or validate CUDA; it only prints the intended Docker command.

## 4. Generate a short WAV (GPU)

```powershell
.\.venv\Scripts\python.exe poc/voice_design.py `
  --text-file examples/orfina-voicedesign-short.txt `
  --output outputs/orfina-voicedesign-q8.wav `
  --quant q8
```

The wrapper mounts the `models/` directory read-only and `outputs/` read-write, disables networking *inside the inference container*, and passes input text over stdin. Inference is local. Its description asks for a gentle, warm female voice with Brazilian Portuguese pronunciation; **accent and voice quality are not guaranteed**.

## 5. What to measure

Check whether Docker can see CUDA, whether Q8 finishes without out-of-memory, time to generate, WAV length, female timbre, Brazilian accent, warmth, and naturalness. Monitor VRAM from another PowerShell using `nvidia-smi -l 1`. You can close VRAM-heavy apps if the GPU runs short.

If **Q8** fails due to VRAM, download the matching Q4 files instead:

```powershell
.\.venv\Scripts\hf.exe download Serveurperso/Qwen3-TTS-GGUF `
  qwen-talker-1.7b-voicedesign-Q4_K_M.gguf `
  qwen-tokenizer-12hz-Q4_K_M.gguf `
  --local-dir models
.\.venv\Scripts\python.exe poc/voice_design.py --quant q4 --text-file examples/orfina-voicedesign-short.txt --output outputs/orfina-voicedesign-q4.wav
```

Q4 files total roughly 1.43 GB **on disk**, not necessarily in GPU memory. Compare quality rather than presuming smaller means equally natural. Saving and reusing Orfina's created voice using a separate cloning model is **out of scope** and requires another validation.

## Limitations

- Executable integration and command construction are locally unit-tested, but no Docker/GPU inference has been run by CI or this authoring environment.
- The quantized VoiceDesign route and its latency, quality and VRAM consumption **require a real on-machine test**.
- Docker can keep some GPU memory occupied while running; it does not bypass the shared hardware limit.
- No additional Ubuntu installation, new NVIDIA driver or FlashAttention installation is required for this proposed path.
