import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "poc" / "clone_voice.py"
spec = importlib.util.spec_from_file_location("clone_voice", SCRIPT)
clone = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clone)


class ReferenceCloneTests(unittest.TestCase):
    def test_consent_required(self):
        with tempfile.TemporaryDirectory() as root:
            args = clone.parse_args(["--reference", str(Path(root) / "voice.wav")])
            with self.assertRaisesRegex(ValueError, "permission"):
                clone.prepare(args)

    def test_missing_audio_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            args = clone.parse_args(["--reference", str(Path(root) / "voice.wav"), "--consent"])
            with self.assertRaisesRegex(ValueError, "Reference file not found"):
                clone.prepare(args)

    def test_reference_and_transcript_loaded(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            (base / "voice.wav").write_bytes(b"dummy")
            (base / "reference.txt").write_text("Olá, sou a Orfina.", encoding="utf-8")
            (base / "script.txt").write_text("Astel, eu te amo.", encoding="utf-8")
            args = clone.parse_args(["--reference", str(base / "voice.wav"),
                "--reference-text-file", str(base / "reference.txt"),
                "--text-file", str(base / "script.txt"), "--consent"])
            self.assertEqual(clone.prepare(args), ("Astel, eu te amo.", "Olá, sou a Orfina."))

    def test_empty_transcript_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            (base / "voice.wav").write_bytes(b"dummy")
            args = clone.parse_args(["--reference", str(base / "voice.wav"), "--consent"])
            with self.assertRaisesRegex(ValueError, "exact transcript"):
                clone.prepare(args)


if __name__ == "__main__":
    unittest.main()
