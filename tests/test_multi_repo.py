#!/usr/bin/env python3
"""
Unit tests for MultiRepoAnalyzer.
"""

import pytest
from unittest.mock import MagicMock, patch
from multi_repo import MultiRepoAnalyzer
from github_agent import GitHubAIBrain


@pytest.fixture
def mock_agent():
    """Create a mock GitHubAIBrain instance."""
    agent = MagicMock(spec=GitHubAIBrain)
    return agent


def test_format_org_report():
    """Test organization report markdown formatting."""
    analyzer = MultiRepoAnalyzer(MagicMock())
    report = {
        "organization": "facebook",
        "repositories_analyzed": 2,
        "total_stars": 150000,
        "total_forks": 35000,
        "total_open_issues": 120,
        "average_activity_score": 85.5,
        "top_repositories": [
            {
                "repository": "facebook/react",
                "health_rating": "🟢 Excellent",
                "activity_score": 95,
                "stars": 120000,
            },
            {
                "repository": "facebook/jest",
                "health_rating": "🟡 Good",
                "activity_score": 76,
                "stars": 30000,
            },
        ],
    }

    formatted = analyzer.format_org_report(report)
    assert "Organization Health Audit: facebook" in formatted
    assert "facebook/react" in formatted
    assert "⭐ 120,000" in formatted


@patch.object(GitHubAIBrain, "_api_request")
@patch.object(GitHubAIBrain, "analyze_repository_health")
def test_organization_analysis(mock_health, mock_api):
    """Test organization_analysis workflow with mocks."""
    agent = GitHubAIBrain(token="mock")
    analyzer = MultiRepoAnalyzer(agent)

    mock_api.return_value = [
        {"full_name": "org/repo1"},
        {"full_name": "org/repo2"},
    ]

    mock_health.side_effect = [
        {"repository": "org/repo1", "stars": 100, "forks": 10, "open_issues": 5, "activity_score": 80, "health_rating": "🟢 Excellent"},
        {"repository": "org/repo2", "stars": 200, "forks": 20, "open_issues": 10, "activity_score": 90, "health_rating": "🟢 Excellent"},
    ]

    res = analyzer.organization_analysis("org", max_repos=2)
    assert res["organization"] == "org"
    assert res["repositories_analyzed"] == 2
    assert res["total_stars"] == 300
    assert res["total_forks"] == 30
    assert res["total_open_issues"] == 15
    assert res["average_activity_score"] == 85.0
