# PR #6 — Kokoro pt-BR female synthetic voice proof of concept

This standalone experiment uses the original synthetic **pf_dora** Brazilian Portuguese preset in [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M). We are **not cloning a real person's voice** and are not attempting to imitate any performer. The model weights are Apache 2.0; review the model and individual voice license before redistribution.

**Not yet tested on the target RTX 2080 SUPER / Windows 11.** Good pronunciation or suitability for Orfina are not guaranteed.

## Windows installation (separate environment)

Avoid upgrading or changing the already working Qwen `.venv`. In PowerShell:

```powershell
git fetch origin
git switch --track origin/feat/kokoro-ptbr-poc
py -3.12 -m venv .venv-kokoro
.\.venv-kokoro\Scripts\python.exe -m pip install --upgrade pip
.\.venv-kokoro\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu128
.\.venv-kokoro\Scripts\python.exe -m pip install kokoro soundfile
.\.venv-kokoro\Scripts\python.exe -m pip check
```

Kokoro relies on phonemization through eSpeak NG on Windows. Install the official Windows x64 eSpeak NG release from [espeak-ng releases](https://github.com/espeak-ng/espeak-ng/releases) if not already installed. Reopen PowerShell after installation; verify `espeak-ng --version`. If Python cannot locate the eSpeak NG shared library, report that error rather than modifying global Python packages or switching to Docker.

## Generate

```powershell
.\.venv-kokoro\Scripts\python.exe poc/kokoro_ptbr.py --text-file examples/orfina-voicedesign-short.txt --output outputs/kokoro-orfina-dora.wav
start .\outputs\kokoro-orfina-dora.wav
```

The first run may download open-weight models and voices. Inference executes locally after downloads.

## Evaluation

Listen for native Brazilian pronunciation, warmth, naturalness and age impression. This is a preset voice, **not custom text-based voice design**, and expressive transitions are a future goal. Do not merge based only on a successful WAV: user listening review matters. Compare against existing Qwen presets, with no speaker cloning.

References:
- [Official Kokoro model card](https://huggingface.co/hexgrad/Kokoro-82M)
- [Official Kokoro repository](https://github.com/hexgrad/kokoro)

## Orfina vows: three-part emotional progression

User listening review approved the `pf_dora` baseline at **speed 1.08** for the formal opening, while noting a slightly serious tone. This is a **voice/pacing experiment**, not a finalized canonical wedding speech. Example text is original, provisional, and should be replaced with the approved vows when ready.

Generate three separate WAVs with one command from the repository root:

```powershell
git pull
.\.venv-kokoro\Scripts\python.exe poc/kokoro_vows.py --dry-run
.\.venv-kokoro\Scripts\python.exe poc/kokoro_vows.py
```

Outputs:

| Part | Input | Speed | Expected mood |
|---|---|---:|---|
| 01-opening | `examples/orfina-vows-opening.txt` | 1.08 | Formal and composed (user-approved setting) |
| 02-intimate | `examples/orfina-vows-intimate.txt` | 1.03 | Slower, affectionate and personal |
| 03-finale | `examples/orfina-vows-finale.txt` | 0.98 | Slower, emotionally vulnerable |

The same **`pf_dora`** synthetic voice is used throughout. Changes in speed/punctuation might convey pacing, but **Kokoro does not guarantee vocal trembling, crying, or emotional control**. Listen to each WAV independently; the script does not concatenate them or alter timbre. These speeds are hypotheses to compare, not artistically validated choices. Report if a slower section sounds older or more robotic.

Run tests with `py -3.12 -m unittest discover -s tests -v`; these offline tests don't synthesize audio.

