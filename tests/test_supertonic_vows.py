import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "poc" / "supertonic_vows.py"
spec = importlib.util.spec_from_file_location("supertonic_vows", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SupertonicVowsTests(unittest.TestCase):
    def test_six_distinct_files_and_consistent_speeds(self):
        with tempfile.TemporaryDirectory() as directory:
            jobs = module.plan(Path(directory))
            self.assertEqual(len(jobs), 6)
            self.assertEqual(len({str(job[4]) for job in jobs}), 6)
            self.assertEqual([job[0] for job in jobs], ["F1"] * 3 + ["F5"] * 3)
            self.assertEqual([job[3] for job in jobs], [1.08, 1.03, 0.98] * 2)

    def test_no_generation_in_dry_run(self):
        self.assertEqual(module.main(["--dry-run"]), 0)


if __name__ == "__main__":
    unittest.main()
