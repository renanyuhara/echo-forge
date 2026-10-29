import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "poc" / "compare_ptbr.py"
spec = importlib.util.spec_from_file_location("compare_ptbr", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ComparePtBrTests(unittest.TestCase):
    def test_two_preset_commands(self):
        cmds = module.commands("python", "generate.py", "text.txt", "outputs", ["serena", "vivian"])
        self.assertEqual(len(cmds), 2)
        self.assertEqual(cmds[0][cmds[0].index("--speaker") + 1], "serena")
        self.assertEqual(cmds[1][cmds[1].index("--speaker") + 1], "vivian")
        self.assertTrue(cmds[1][-1].endswith("ptbr-vivian.wav"))
        self.assertIn("float32", cmds[0])

    def test_dry_run_without_model_loading(self):
        with tempfile.TemporaryDirectory() as folder:
            text_file = Path(folder) / "text.txt"
            text_file.write_text("Olá, Astel!", encoding="utf-8")
            self.assertEqual(module.main(["--text-file", str(text_file), "--dry-run"]), 0)

if __name__ == "__main__":
    unittest.main()
