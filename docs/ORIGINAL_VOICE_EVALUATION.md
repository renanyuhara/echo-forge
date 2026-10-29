# Original Brazilian Portuguese voice evaluation

## Decision
EchoForge creates **original fictional character voices**. No voice imitation, performer cloning, or scraped actor samples are part of the Orfina workflow. Artistic inspiration may guide descriptions but must not become speaker imitation.

## Findings
- Qwen3-TTS 1.7B VoiceDesign GGUF Q8: passed Windows + Docker + RTX 2080 SUPER runtime test (5.76 seconds WAV in 40.36 seconds), but user judged Brazilian accent to sound foreign.
- Qwen3-TTS 0.6B CustomVoice: female Vivian had relatively better Brazilian pronunciation; Serena was softer but substantially more accented.
- Qwen3-TTS Base is a reference-cloning architecture, **not an original text-to-voice identity generator**. It is not our next experiment.

## Candidates and caveats

| Candidate | Native pt-BR | New voice without reference | Purpose |
|---|---|---|---|
| Qwen3-TTS VoiceDesign 1.7B | Portuguese supported, accent failed initial test | Yes | Baseline, no further work without a specific new hypothesis |
| Qwen3-TTS CustomVoice 0.6B | Some preset speakers sound better | Preset identities, not arbitrary design | Benchmark pronunciation and quality |
| Kokoro multilingual pt-BR voices | Community integrations advertise native pt-BR voices; verify upstream license/models | Preset voice, not custom identity creation | Candidate low-VRAM baseline |
| Piper pt_BR voice packs | pt-BR packages exist; verify model license and quality | Preset voices | Fast baseline, may be insufficiently expressive |

**Do not** recommend F5-TTS/XTTS/Chatterbox cloning as voice-design substitutes. They may require a reference recording, which is distinct from original voice creation. Treat newly advertised options as unverified until tested.

## Evaluation gate
1. Inventory a downloadable, licensed native pt-BR female **synthetic preset** or genuine text-described voice-design model.
2. Test generation locally on Windows, with the RTX 2080 SUPER and no private recordings.
3. Compare the same 2–3 short Portuguese phrases (including Orfina dialogue).
4. Rate Brazilian pronunciation, timbre maturity, softness, expressivity, identity stability, inference time, VRAM.
5. Prefer excellent pt-BR quality over unconstrained voice-design flexibility. Do not merge an engine unless it passes listening review.

## Original Orfina target
Mature, warm, soft and naturally feminine, refined articulation inherited from a noble upbringing; affectionate and deeply emotive in private. For vows: composed formal opening, intimacy and warmth, memories and vulnerability, then tearful but sincere emotional release. Native Brazilian Portuguese without theatrical or childish delivery.

## Status
The new experiments are **planning only**; no new voice engine has been validated. The previous reference-cloning prototype on this feature branch is **out of scope** and should not be used for Orfina.
