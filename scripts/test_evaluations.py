"""Protect retained skill-trial evidence from accidental formatting or loss.

Raw snapshots establish what an agent actually received and produced. Compare
their bytes with the recorded hashes rather than current skill implementations;
historical failures remain evidence when a skill changes.
"""

import hashlib
import json
from pathlib import Path
import unittest


RECORDS = Path(__file__).resolve().parent.parent / "evaluations"
ARCHIVES = ("writing", "discovery")


class EvaluationArchiveTests(unittest.TestCase):
    """Keep every archived skill trial represented by its original bytes."""

    def test_recorded_trial_assets_retain_their_original_bytes(self):
        """Detect missing trials, duplicate identities, and changed raw assets."""
        self.assertEqual(set(ARCHIVES), {item.name for item in RECORDS.iterdir() if item.is_dir()})
        for archive in ARCHIVES:
            records = RECORDS / archive
            manifest = json.loads((records / "manifest.json").read_text())
            cases = [entry["case"] for entry in manifest]
            self.assertEqual(len(cases), len(set(cases)), f"Duplicate trial identity in {archive}")
            self.assertEqual(set(cases), {item.name for item in records.iterdir() if (item / "skill.txt").is_file()})
            for entry in manifest:
                assets = {f"{name}.txt": entry[f"{name}_sha256"] for name in ("skill", "task", "output")}
                assets.update(entry.get("additional_sha256", {}))
                for filename, expected in assets.items():
                    with self.subTest(archive=archive, case=entry["case"], asset=filename):
                        asset = records / entry["case"] / filename
                        self.assertTrue(asset.is_file(), f"Missing trial evidence: {asset}")
                        self.assertEqual(hashlib.sha256(asset.read_bytes()).hexdigest(), expected)


if __name__ == "__main__":
    unittest.main()
