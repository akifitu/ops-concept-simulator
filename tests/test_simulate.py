"""Regression tests for the ConOps simulator."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ops_concept_simulator.cli import run
from ops_concept_simulator.data import load_scenarios
from ops_concept_simulator.simulate import analyze_scenarios


DATA_FILE = ROOT / "data" / "scenarios.json"


class ConOpsTests(unittest.TestCase):
    def test_clean_dataset_passes(self) -> None:
        result = analyze_scenarios(load_scenarios(DATA_FILE))
        self.assertEqual(result.errors, [])
        self.assertEqual(result.summary["scenario_count"], 3)

    def test_negative_duration_is_detected(self) -> None:
        scenarios = load_scenarios(DATA_FILE)
        scenarios[0]["phases"][0]["duration_hours"] = 0
        result = analyze_scenarios(scenarios)
        self.assertTrue(any("duration_hours must be greater than zero" in item for item in result.errors))

    def test_cli_exports_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            exit_code = run(["simulate", "--data-file", str(DATA_FILE), "--export-dir", temp_dir])
            self.assertEqual(exit_code, 0)
            export_dir = Path(temp_dir)
            self.assertTrue((export_dir / "conops-summary.md").exists())
            self.assertTrue((export_dir / "scenario-catalog.csv").exists())
            self.assertTrue((export_dir / "subsystem-utilization.csv").exists())
            self.assertTrue((export_dir / "conops-dashboard.html").exists())


if __name__ == "__main__":
    unittest.main()
