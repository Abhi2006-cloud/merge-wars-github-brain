#!/usr/bin/env python3
"""
🧪 Unit test suite for GitHub CLI interface and command-line flags.
"""

import unittest
from unittest.mock import MagicMock, patch
from cli_interface import GitHubCLI


class TestGitHubCLI(unittest.TestCase):
    """Test suite for CLI argument parsing and execution."""

    def setUp(self):
        self.cli = GitHubCLI()

    @patch("cli_interface.GitHubAIBrain.analyze_repository_health")
    def test_analyze_flag(self, mock_analyze):
        """Test --analyze flag invocation."""
        mock_analyze.return_value = {
            "repository": "test/repo",
            "stars": 100,
            "forks": 10,
            "open_issues": 5,
            "open_prs": 2,
            "recent_commits": 8,
            "activity_score": 85,
            "health_rating": "🟢 Excellent",
        }
        self.cli.run(["--analyze", "test/repo"])
        mock_analyze.assert_called_once_with("test/repo")

    @patch("cli_interface.GitHubAIBrain.compare_repositories")
    def test_compare_flag(self, mock_compare):
        """Test --compare flag invocation."""
        mock_compare.return_value = {
            "comparison_date": "2026-08-14T00:00:00Z",
            "repositories_analyzed": 2,
            "detailed_analysis": {
                "repo1/test": {"health_rating": "🟢 Excellent", "activity_score": 90, "stars": 100},
                "repo2/test": {"health_rating": "🟡 Good", "activity_score": 70, "stars": 50},
            },
            "ranking": ["repo1/test", "repo2/test"],
        }
        self.cli.run(["--compare", "repo1/test", "repo2/test"])
        mock_compare.assert_called_once_with(["repo1/test", "repo2/test"])

    @patch("cli_interface.MultiRepoAnalyzer.organization_analysis")
    def test_org_flag(self, mock_org):
        """Test --org flag invocation."""
        mock_org.return_value = {
            "organization": "testorg",
            "repositories_analyzed": 1,
            "total_stars": 50,
            "total_forks": 5,
            "total_open_issues": 2,
            "average_activity_score": 75.0,
            "top_repositories": [],
        }
        self.cli.run(["--org", "testorg"])
        mock_org.assert_called_once_with("testorg")

    @patch("cli_interface.GitHubAIBrain.query")
    def test_query_flag(self, mock_query):
        """Test --query flag invocation."""
        mock_query.return_value = "Query test output"
        self.cli.run(["--query", "Analyze test/repo"])
        mock_query.assert_called_once_with("Analyze test/repo")


if __name__ == "__main__":
    unittest.main()
