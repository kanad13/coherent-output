"""Protect retained skill-trial evidence from accidental formatting or loss.

Raw snapshots establish what an agent actually received and produced. Compare
their bytes with the recorded hashes rather than current skill implementations;
historical failures remain evidence when a skill changes.
"""

import hashlib
import json
from pathlib import Path
import unittest


RECORDS = Path(__file__).resolve().parent.parent / "evaluations/writing"


class EvaluationArchiveTests(unittest.TestCase):
    """Keep every archived writing trial represented by its original bytes."""

    def test_recorded_trial_assets_retain_their_original_bytes(self):
        """Detect missing trials, duplicate identities, and changed raw assets."""
        manifest = json.loads((RECORDS / "manifest.json").read_text())
        cases = [entry["case"] for entry in manifest]
        self.assertEqual(len(cases), len(set(cases)), "Duplicate trial identity")
        self.assertEqual(set(cases), {item.name for item in RECORDS.iterdir() if (item / "skill.txt").is_file()})
        for entry in manifest:
            assets = {f"{name}.txt": entry[f"{name}_sha256"] for name in ("skill", "task", "output")}
            assets.update(entry.get("additional_sha256", {}))
            for filename, expected in assets.items():
                with self.subTest(case=entry["case"], asset=filename):
                    asset = RECORDS / entry["case"] / filename
                    self.assertTrue(asset.is_file(), f"Missing trial evidence: {asset}")
                    self.assertEqual(hashlib.sha256(asset.read_bytes()).hexdigest(), expected)


if __name__ == "__main__":
    unittest.main()
