"""Offline unit tests: no Docker, GPU or weights needed."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "poc" / "voice_design.py"
spec = importlib.util.spec_from_file_location("voice_design", MODULE)
voice_design = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voice_design)


class VoiceDesignCommandTests(unittest.TestCase):
    def make_args(self, root, extra=None):
        root = Path(root)
        (root / "test.txt").write_text("Orfina abraça Astel.", encoding="utf-8")
        return voice_design.parser().parse_args(
            ["--models-dir", str(root), "--text-file", str(root / "test.txt"),
             "--output", str(root / "out" / "result.wav")] + (extra or [])
        )

    def test_command_uses_cuda_no_network_q8(self):
        with tempfile.TemporaryDirectory() as directory:
            args = self.make_args(directory, ["--dry-run"])
            command, script, output = voice_design.docker_command(args)
            self.assertEqual(script, "Orfina abraça Astel.")
            self.assertEqual(output.name, "result.wav")
            self.assertEqual(command[command.index("--gpus") + 1], "all")
            self.assertEqual(command[command.index("--network") + 1], "none")
            self.assertEqual(command[command.index("--device") + 1], "CUDA0")
            self.assertIn("/models/qwen-talker-1.7b-voicedesign-Q8_0.gguf", command)
            self.assertIn("/models/qwen-tokenizer-12hz-Q8_0.gguf", command)

    def test_q4_uses_matching_talker_and_tokenizer(self):
        with tempfile.TemporaryDirectory() as directory:
            args = self.make_args(directory, ["--dry-run", "--quant", "q4"])
            command, _, _ = voice_design.docker_command(args)
            self.assertIn("/models/qwen-talker-1.7b-voicedesign-Q4_K_M.gguf", command)
            self.assertIn("/models/qwen-tokenizer-12hz-Q4_K_M.gguf", command)

    def test_requires_weights_for_real_run(self):
        with tempfile.TemporaryDirectory() as directory:
            args = self.make_args(directory)
            with self.assertRaisesRegex(ValueError, "Required GGUF"):
                voice_design.docker_command(args)

    def test_dry_run_has_no_output_side_effect(self):
        with tempfile.TemporaryDirectory() as directory:
            args = self.make_args(directory, ["--dry-run"])
            command, _, output = voice_design.docker_command(args)
            self.assertFalse(output.parent.exists())
            self.assertEqual(command[0], "docker")


if __name__ == "__main__":
    unittest.main()
