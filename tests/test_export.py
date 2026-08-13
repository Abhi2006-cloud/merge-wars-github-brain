#!/usr/bin/env python3
"""
🧪 Unit test suite for report JSON/CSV export functionality.
"""

import os
import json
import csv
import unittest
import tempfile
from github_agent import GitHubAIBrain


class TestExportFunctionality(unittest.TestCase):
    """Test suite verifying export_report_json and export_report_csv."""

    def setUp(self):
        self.agent = GitHubAIBrain()
        self.sample_data = {
            "repository": "test/repo",
            "description": "A sample repository for testing exports",
            "health_rating": "🟢 Excellent",
            "activity_score": 90,
            "stars": 1200,
            "forks": 150,
            "open_issues": 3,
            "open_prs": 1,
            "recent_commits": 15,
            "last_updated": "2026-08-14T00:00:00Z",
        }
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_export_to_json(self):
        """Verify JSON export creates a valid readable JSON file."""
        filepath = os.path.join(self.temp_dir.name, "output.json")
        result_path = self.agent.export_report_json(self.sample_data, filepath)

        self.assertTrue(os.path.exists(result_path))
        with open(result_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["repository"], "test/repo")
            self.assertEqual(data["activity_score"], 90)

    def test_export_to_csv(self):
        """Verify CSV export creates a valid readable CSV file."""
        filepath = os.path.join(self.temp_dir.name, "output.csv")
        result_path = self.agent.export_report_csv(self.sample_data, filepath)

        self.assertTrue(os.path.exists(result_path))
        with open(result_path, "r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
            self.assertGreater(len(reader), 1)
            self.assertEqual(reader[0], ["Metric", "Value"])


if __name__ == "__main__":
    unittest.main()
