"""Check the structure rules of the mermaid-architect verifier without a browser.

Each case is a reviewed defect (islands, boxed islands passing as related, compound
caption, reversed direction) or the fix that must stay accepted.
"""

import importlib.util
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("verifier", SOURCE / "skills/mermaid-architect/scripts/verify-markdown.py")
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)

ISLANDS = 'flowchart LR\nA["Sales reports"] --> B["Sales Operations"]\nC["Finance reports"] --> D["Controlling"]'
HUB = 'flowchart LR\nC["Customer"] -->|"Gold plan"| P["Phone line"]\nC -->|"Basic plan"| E["Email form"]'
OUTER_BOX = 'flowchart TB\nsubgraph S ["Support by plan"]\nsubgraph G ["Gold plan"]\nP["Phone line"]\nend\nsubgraph B ["Basic plan"]\nE["Email form"]\nend\nend'
REVERSED = 'flowchart RL\nS["Suppliers"] --> P["Plant"] --> R["Retailers"]'
TOO_BIG = "flowchart LR\n" + "\n".join(f'N{i}["Node {i}"] --> N{i + 1}["Node {i + 1}"]' for i in range(0, 12, 2)) + "\nN1 --> N2\nN3 --> N4\nN5 --> N6\nN7 --> N8\nN9 --> N10"
QUOTED_SEQUENCE = 'sequenceDiagram\nA->>B: "Deliver parts"'


def check(code, caption=None):
    return verifier.check_structure(caption, code)


class StructureChecks(unittest.TestCase):
    """Pin each rule to a reviewed example."""

    def test_islands_fail(self):
        self.assertTrue(any("disconnected" in e for e in check(ISLANDS)[0]))

    def test_hub_and_outer_box_pass(self):
        self.assertEqual(check(HUB)[0], [])
        self.assertEqual(check(OUTER_BOX)[0], [])

    def test_reversed_direction_fails(self):
        self.assertTrue(any("RL" in e for e in check(REVERSED)[0]))

    def test_node_limit_fails(self):
        self.assertTrue(any("nodes exceed" in e for e in check(TOO_BIG)[0]))

    def test_compound_caption_warns_without_failing(self):
        errors, warnings = check(HUB, "Gold customers get a phone line, while Basic customers use email.")
        self.assertEqual(errors, [])
        self.assertTrue(any("compound" in w for w in warnings))

    def test_single_relation_caption_is_clean(self):
        self.assertEqual(check(HUB, "A customer's plan decides which support channel applies.")[1], [])

    def test_quoted_sequence_message_warns(self):
        self.assertTrue(any("quotes" in w for w in check(QUOTED_SEQUENCE)[1]))

    def test_unclosed_fence_is_reported(self):
        self.assertTrue(verifier.parse_blocks("```mermaid\nflowchart LR\nA --> B\n")[1])


if __name__ == "__main__":
    unittest.main()
