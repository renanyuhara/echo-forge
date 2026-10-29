import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "poc" / "supertonic_pt.py"
spec = importlib.util.spec_from_file_location("supertonic_pt", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class SupertonicPtTests(unittest.TestCase):
    def test_dry_run_no_model(self):
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "sample.txt"
            sample.write_text("Astel, eu estou aqui.", encoding="utf-8")
            self.assertEqual(module.main(["--text-file", str(sample), "--dry-run"]), 0)

    def test_default_voices(self):
        self.assertEqual(module.parse_args([]).voices, ["F1", "F2", "F3", "F4", "F5"])

    def test_rejects_invalid_speed(self):
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "sample.txt"
            sample.write_text("Olá.", encoding="utf-8")
            with self.assertRaises(SystemExit):
                module.main(["--text-file", str(sample), "--speed", "4", "--dry-run"])

if __name__ == "__main__":
    unittest.main()
