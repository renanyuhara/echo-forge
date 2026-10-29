# Supertonic 3 — original female Portuguese voices

We are testing five **built-in synthetic voices F1–F5**, *not cloning or imitating anyone*. The target is a softer, younger-sounding, more delicate timbre than Kokoro's `pf_dora`, with natural Brazilian Portuguese pronunciation.

**Caveat:** Supertonic supports multilingual Portuguese (`pt`); it does not advertise a guaranteed Brazilian regional accent. The accent, naturalness and voice suitability are **unverified** until listening tests. Built-in voice style does not mean a new text-prompt-designed identity.

## Windows PowerShell

Keep Qwen's `.venv` and Kokoro's `.venv-kokoro` unchanged. Create a third isolated environment:

```powershell
git fetch origin
git switch --track origin/feat/supertonic-female-pt-poc
py -3.12 -m venv .venv-supertonic
.\.venv-supertonic\Scripts\python.exe -m pip install supertonic
.\.venv-supertonic\Scripts\python.exe -m pip check
.\.venv-supertonic\Scripts\python.exe -m unittest discover -s tests -v
.\.venv-supertonic\Scripts\python.exe poc/supertonic_pt.py --dry-run
.\.venv-supertonic\Scripts\python.exe poc/supertonic_pt.py
```

The first synthesis downloads roughly 400 MB of model data. The backend uses local CPU ONNX inference; **GPU is not required**. Output: `outputs/supertonic-pt/f1.wav` through `f5.wav`. Listen to all five and compare against the existing Kokoro Dora baseline. Please report the voice(s) that feel mature but young, soft, delicate and emotionally capable, and whether any have an unacceptable Portuguese accent.

If a single candidate wins, we will test a three-part emotional speech using the approved timing, without assuming the model can cry or follow emotional instructions. No download/re-recording of performer voices is part of the workflow.

Official package docs: https://github.com/supertone-oss-archive/supertonic-py/blob/main/docs/quickstart.md
Upstream model: https://huggingface.co/Supertone/supertonic
Check model license before shipping model assets or using generated audio commercially. The open-source project and its licensing should be evaluated separately.
