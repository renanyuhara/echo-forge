# EchoForge — Product Specification

**Status:** Draft v0.1 · **Updated:** 2026-10-29  
**Product language:** English for code, documentation, and identifiers; **initial generated speech:** Brazilian Portuguese (pt-BR).

## 1. Vision

EchoForge is a local-first AI voice studio for RPG characters, storytelling, and immersive narratives. Users write dialogue, choose a persistent character voice, generate speech on their own computer, preview takes, and export audio for use during sessions.

**First use case:** create Orfina's wedding vows to Astel in Brazilian Portuguese with an expressive, recognizable voice that can be reused in future scenes.

This is a standalone application, not a module of RPG Codex or TDA. Optional integrations may follow later.

## 2. Goals

- Run voice inference locally, without a mandatory paid cloud API.
- Target Windows 11 + WSL2 and an NVIDIA RTX 2080 SUPER (8 GB VRAM).
- Produce intelligible, natural-sounding **pt-BR** speech.
- Support creating a voice from a descriptive prompt, then saving an approved sample as its reference.
- Support reference-audio voice cloning, with appropriate consent and rights.
- Persist character voice profiles, reference samples, generation settings and output history locally.
- Allow multiple takes, playback, and WAV export.
- Keep the inference engine replaceable: favor model adapters rather than binding domain data to a single model.

## 3. Non-goals for the MVP

- Training a foundation model from scratch or requiring fine-tuning per character.
- Real-time voice conversion, microphone-to-microphone streaming, multiplayer hosting, or public deployment.
- Automatic voice matching to a real actor without authorization.
- Guaranteed identical pronunciation, emotion, or speaker identity across runs.
- Built-in music, full soundtrack mixing, or integration with other RPG services.
- MP3 export and advanced timeline editing (post-MVP).

## 4. Proposed user workflow

1. Create a **character** (e.g. Orfina) and record a short description.
2. Create or import a **voice reference**:
   - **Voice design:** describe desired age impression, pitch, timbre, rhythm, accent and attitude; synthesize candidate samples using an engine that actually supports voice design.
   - **Reference audio:** import a clean recording that the user owns or is authorized to use.
3. Preview candidates; explicitly approve one as a character's active reference.
4. Enter a passage in **pt-BR**, choose the character voice and available settings.
5. Generate one or more takes, listen, compare, and download a WAV.
6. Later, reuse the saved character and its active reference to generate new dialogue.

**Important:** reference-audio cloning and text-described voice design are distinct capabilities; a TTS model that clones voices does not necessarily generate new speaker identities from text prompts. The final model selection must validate both workflows rather than assume interchangeability.

## 5. MVP acceptance criteria

- [ ] A developer can install documented dependencies and start the application locally under the target setup.
- [ ] The application detects CUDA availability and reports GPU/VRAM and useful errors; it never falsely claims GPU acceleration.
- [ ] An end-to-end local pt-BR text-to-WAV generation succeeds on the target RTX 2080 SUPER.
- [ ] A user can add/edit/delete a character and associate one or more voice samples.
- [ ] A user can import, preview, and designate an authorized voice reference as active.
- [ ] The application supports creating a voice through a *validated* voice-design model, or clearly marks this feature unavailable until that adapter is ready.
- [ ] A user can generate, play, and download at least one WAV take, with actionable error messages.
- [ ] Output history identifies the source text, selected character, model/version, parameters and reference used.
- [ ] Model weights, reference files, and generated audio stay outside Git; model downloads are explicit and locally stored.
- [ ] The app binds to localhost by default and does not upload scripts or voice data to third-party services.
- [ ] A qualitative manual evaluation compares pronunciation, consistency, emotional expressiveness, inference time and peak VRAM on realistic Portuguese dialogue.

## 6. Technical direction (provisional)

- **UI:** small local web interface; final framework TBD after the inference proof of concept.
- **Backend:** Python service for model inference, audio preprocessing, and file operations.
- **Runtime:** Python + PyTorch + CUDA on WSL2, subject to driver, dependency and model compatibility checks.
- **Storage:** local application data directory (metadata may begin as JSON/SQLite); preserve stable references to characters and approved voice samples.
- **Inference:** model-adapter abstraction exposing capabilities such as voice design, reference cloning, language, and available generation parameters.
- **Output:** uncompressed WAV for the MVP; avoid embedding personal reference recordings in repository fixtures.

Candidate engines for evaluation (not yet approved as implementation decisions):
- **Qwen3-TTS:** investigate the specific VoiceDesign and cloning model variants, their hardware requirements and pt-BR quality.
- **Chatterbox Multilingual:** investigate reference cloning, supported Portuguese accent quality, emotional controls, and 8 GB VRAM compatibility.
- **XTTS-v2:** optional baseline for reference cloning and pt-BR.

The first engineering milestone is a reproducible CLI inference spike with measured peak VRAM and listening tests. **Do not select a production engine solely on advertised language support**; check actual Brazilian pronunciation, licensing, dependencies and reproducibility on the target GPU.

## 7. Data entities (conceptual)

- **Character:** ID, name, optional description, active voice reference ID.
- **VoiceReference:** ID, origin (designed/imported), original or generated audio path, description, approval status, provenance/consent note, associated model metadata.
- **Generation:** ID, character ID, script, language, model ID/version, parameters, voice reference ID, output path, timestamp, status/error.

Local file deletion and reference replacement should not silently break historical generation records. Avoid raw audio or text in logs by default.

## 8. Privacy, rights and safety

- Use only voice samples owned by the user or recorded/shared with permission. Avoid cloning identifiable people's voices without consent.
- Store reference audio and generated outputs locally; provide a way to delete them.
- Show the active voice's provenance or consent status.
- Do not commit recordings, private scripts, downloaded weights, caches, or generated assets.
- Clearly identify AI-generated audio when sharing it in contexts where confusion might matter.
- Review each selected model's license before redistribution or bundling weights.

## 9. Milestones

**M0 — Specification (this PR):** README, product scope, acceptance criteria, candidate model evaluation plan.

**M1 — Inference spike:** bootstrap environment; validate GPU and one complete pt-BR generation; compare voices/VRAM/performance and record chosen engine.

**M2 — Local MVP:** character/reference library, generation UI, playback, persistent data, WAV export, basic errors and tests.

**M3 — Narrative quality:** voice design flow, expressive takes, pronunciation tuning, consistency evaluations and optional MP3 export.

**M4 — Optional integrations:** RPG Codex/TDA or batch scripting only after the local workflow is stable.

## 10. Open decisions

- Which exact model/variant provides both voice design and reference-based cloning satisfactorily on 8 GB VRAM?
- Do we need CPU fallback or is a supported NVIDIA GPU mandatory for v1?
- Which local UI framework and metadata store minimize setup and maintenance?
- How should long scripts be chunked while keeping tone and speaker identity consistent?
- Which experimental controls genuinely improve expressive pt-BR results?
- What installation method should eventually be supported on Windows (WSL command, launcher, or packaged desktop app)?

**Decision principle:** ship the smallest reproducible local workflow first; validate model capabilities and hardware before committing to a larger architecture.
