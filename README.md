# EchoForge

**Where characters find their voice.**

A local-first AI voice studio for RPG characters, storytelling, and immersive narratives.

EchoForge aims to turn written dialogue into expressive speech with reusable character voices — generated on your own computer, without requiring a paid cloud TTS service.

## First scenario

Create **Orfina's wedding vows to Astel** in Brazilian Portuguese, select and save her voice, and reuse it for future RPG scenes.

## Planned MVP

- Local text-to-speech in **Brazilian Portuguese (pt-BR)**
- Create or import a character voice reference (subject to engine support)
- Character and voice library
- Generate, preview, compare and download WAV takes
- Local storage of references and outputs
- GPU inference targeted at **Windows 11 + WSL2 + NVIDIA RTX 2080 SUPER (8 GB)**

> **Status:** specification phase. Model support, quality and target GPU compatibility have not yet been validated. No working audio generation is included yet.

## Documentation

- [Product specification, acceptance criteria and roadmap](docs/PRODUCT_SPEC.md)

## Development approach

Start by verifying a local pt-BR inference pipeline and benchmarking candidate engines before choosing the permanent backend and interface. Keep the inference engine modular, and avoid committing voice samples, model weights or generated audio.

## Privacy and responsible use

Use only voice references you own or have permission to use. Voice samples and generated assets will remain local by default; optional integrations will be considered only after the standalone application works reliably.

## License

Not yet selected. Licensing of model weights and code must be reviewed before redistribution.
