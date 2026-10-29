import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "poc" / "kokoro_vows.py"
spec = importlib.util.spec_from_file_location("kokoro_vows", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class KokoroVowsTests(unittest.TestCase):
    def test_commands_are_distinct_with_progression(self):
        commands = module.build_commands("python", "outputs/test", "cpu")
        self.assertEqual(len(commands), 3)
        self.assertEqual([x[x.index("--speed") + 1] for x in commands], ["1.08", "1.03", "0.98"])
        self.assertEqual([x[x.index("--voice") + 1] for x in commands], ["pf_dora"] * 3)
        self.assertTrue(commands[0][commands[0].index("--output") + 1].endswith("01-opening.wav"))
        self.assertTrue(commands[2][commands[2].index("--output") + 1].endswith("03-finale.wav"))

    def test_dry_run(self):
        self.assertEqual(module.main(["--dry-run", "--device", "cpu"]), 0)


if __name__ == "__main__":
    unittest.main()
