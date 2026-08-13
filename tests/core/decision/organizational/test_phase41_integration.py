import unittest
from pathlib import Path


class Phase41IntegrationBoundaryTests(unittest.TestCase):
    ROOT = Path(__file__).resolve().parents[3]

    def test_existing_phase_boundaries_remain_present(self):
        for path in (
            "app/api/core/decision",
            "app/api/core/organization",
            "app/api/core/knowledge_synthesis",
            "app/api/core/learning",
            "app/api/core/release",
        ):
            self.assertTrue((self.ROOT / path).exists(), path)

    def test_phase24_execution_is_boundary_only(self):
        source = (self.ROOT / "app/api/core/decision/organizational/__init__.py").read_text(encoding="utf-8")
        self.assertIn("PHASE_24_EXECUTION_BOUNDARY", source)
        self.assertIn("authorization_reference", source)


if __name__ == "__main__":
    unittest.main()
