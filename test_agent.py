#!/usr/bin/env python3
"""
🧪 Integration test suite for GitHub AI Brain.
"""

import unittest
from github_agent import GitHubAIBrain
from multi_repo import MultiRepoAnalyzer


class TestGitHubAIBrainIntegration(unittest.TestCase):
    """Integration test suite verifying core agent functionality."""

    @classmethod
    def setUpClass(cls):
        cls.agent = GitHubAIBrain()
        cls.multi_analyzer = MultiRepoAnalyzer(cls.agent)

    def test_query_repository_health(self):
        """Verify health query returns structured markdown output."""
        response = self.agent.query("Analyze microsoft/vscode")
        self.assertIn("Repository Health Report", response)
        self.assertIn("microsoft/vscode", response)

    def test_query_repository_comparison(self):
        """Verify comparative benchmarking returns ranking."""
        response = self.agent.query("Compare tensorflow/tensorflow vs pytorch/pytorch")
        self.assertIn("Repository Benchmarking Report", response)
        self.assertIn("tensorflow/tensorflow", response)

    def test_query_organization_audit(self):
        """Verify organization query routing."""
        response = self.agent.query("Analyze organization facebook")
        self.assertIn("Organization Health Audit", response)

    def test_query_unknown_format(self):
        """Verify fallback help menu for ambiguous queries."""
        response = self.agent.query("Unknown random text without repo")
        self.assertIn("Help & Command Reference", response)


if __name__ == "__main__":
    unittest.main()
