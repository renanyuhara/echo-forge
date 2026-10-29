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


## F1 vs F5 — Three moments of Orfina's vows

The user approved **F1 and F5** as the two strongest candidates in the first listening test. This new experiment renders both across the **same three provisional texts** and **identical speed per scene**, so the timbre can be compared fairly. These are example texts, not canonical final vows.

From `C:\projects\echo-forge` in PowerShell, on this PR's branch:

```powershell
git pull
.\.venv-supertonic\Scripts\python.exe -m unittest discover -s tests -v
.\.venv-supertonic\Scripts\python.exe poc/supertonic_vows.py --dry-run
.\.venv-supertonic\Scripts\python.exe poc/supertonic_vows.py
explorer .\outputs\supertonic-vows
```

The six output files are:
- `outputs/supertonic-vows/f1/01-opening.wav`
- `outputs/supertonic-vows/f1/02-intimate.wav`
- `outputs/supertonic-vows/f1/03-finale.wav`
- `outputs/supertonic-vows/f5/01-opening.wav`
- `outputs/supertonic-vows/f5/02-intimate.wav`
- `outputs/supertonic-vows/f5/03-finale.wav`

Scenes use the **same relative speeds** as the earlier Kokoro experiment: opening `1.08`, intimate `1.03`, finale `0.98`. These numeric speed settings are a starting hypothesis, not guaranteed to have identical effects across engines. Supertonic does not guarantee controllable crying or emotional expression. Listen for a voice that stays **soft, delicate, adult but not old**, naturally Brazilian and believable in all three moments.

No extra packages or recorded voice samples are required after the first Supertonic evaluation.
