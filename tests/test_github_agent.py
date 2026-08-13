#!/usr/bin/env python3
"""
Unit tests for GitHubAIBrain core logic and helpers.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta
from github_agent import GitHubAIBrain


@pytest.fixture
def agent():
    """Create a GitHubAIBrain instance for testing."""
    return GitHubAIBrain(token="mock_token")


def test_is_recent(agent):
    """Test date recency evaluation logic."""
    now_utc = datetime.now(timezone.utc)
    recent_date = (now_utc - timedelta(days=5)).isoformat()
    old_date = (now_utc - timedelta(days=40)).isoformat()

    assert agent._is_recent(recent_date, days=30) is True
    assert agent._is_recent(old_date, days=30) is False
    assert agent._is_recent(None) is False
    assert agent._is_recent("invalid-date-string") is False


def test_calculate_activity_score(agent):
    """Test weighted activity score calculation."""
    recent = datetime.now(timezone.utc).isoformat()
    old = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()

    commits = [{"commit": {"author": {"date": recent}}}] * 5
    issues = [{"updated_at": recent}] * 10
    prs = [{"updated_at": recent}] * 4

    # 5 commits * 8 = 40 (max)
    # 10 issues * 3 = 30 (max)
    # 4 prs * 5 = 20
    # Total = 90
    score = agent._calculate_activity_score(commits, issues, prs)
    assert score == 90

    # Zero activity case
    old_commits = [{"commit": {"author": {"date": old}}}]
    assert agent._calculate_activity_score(old_commits, [], []) == 0


def test_analyze_workflows(agent):
    """Test workflow run status aggregation."""
    workflows = [
        {"conclusion": "success", "status": "completed"},
        {"conclusion": "failure", "status": "completed"},
        {"conclusion": "success", "status": "completed"},
    ]
    res = agent._analyze_workflows(workflows)
    assert res["total_runs"] == 3
    assert res["statuses"]["success"] == 2
    assert res["statuses"]["failure"] == 1
    assert res["latest_status"] == "success"

    # Empty workflow case
    empty_res = agent._analyze_workflows([])
    assert empty_res["total_runs"] == 0
    assert empty_res["latest_status"] == "N/A"


def test_extract_repository(agent):
    """Test repository identifier parsing."""
    assert agent._extract_repository("Analyze microsoft/vscode now") == "microsoft/vscode"
    assert agent._extract_repository("Show issues in facebook/react") == "facebook/react"
    assert agent._extract_repository("No repository specified here") is None


def test_extract_multiple_repositories(agent):
    """Test parsing multiple repository identifiers."""
    query = "Compare tensorflow/tensorflow vs pytorch/pytorch and huggingface/transformers"
    repos = agent._extract_multiple_repositories(query)
    assert repos == ["tensorflow/tensorflow", "pytorch/pytorch", "huggingface/transformers"]


def test_extract_org_name(agent):
    """Test organization name extraction."""
    assert agent._extract_org_name("Analyze organization facebook") == "facebook"
    assert agent._extract_org_name("Show org google repos") == "google"


@patch.object(GitHubAIBrain, "_api_request")
def test_analyze_repository_health_mocked(mock_api, agent):
    """Test analyze_repository_health with mocked API calls."""
    mock_api.side_effect = [
        # repo info
        {"stargazers_count": 1000, "forks_count": 200, "updated_at": "2026-08-01T00:00:00Z", "description": "Test Repo"},
        # issues
        [{"number": 1, "title": "Test Issue", "updated_at": datetime.now(timezone.utc).isoformat()}],
        # prs
        [{"number": 2, "title": "Test PR", "updated_at": datetime.now(timezone.utc).isoformat()}],
        # commits
        [{"sha": "abc1234", "commit": {"author": {"date": datetime.now(timezone.utc).isoformat()}, "message": "feat: test"}}],
        # workflows
        {"workflow_runs": [{"conclusion": "success", "status": "completed", "name": "CI"}]},
    ]

    res = agent.analyze_repository_health("owner/test-repo")
    assert res["repository"] == "owner/test-repo"
    assert res["stars"] == 1000
    assert res["forks"] == 200
    assert "health_rating" in res
    assert res["activity_score"] > 0


@patch.object(GitHubAIBrain, "analyze_repository_health")
def test_vscode_query_routing(mock_health, agent):
    """Test that queries containing 'vscode' route to health analysis and not comparison."""
    mock_health.return_value = {
        "repository": "microsoft/vscode",
        "stars": 150000,
        "forks": 25000,
        "open_issues": 100,
        "open_prs": 20,
        "recent_commits": 30,
        "activity_score": 95,
        "health_rating": "🟢 Excellent",
    }
    response = agent.query("What is the health status of microsoft/vscode?")
    assert "Repository Health Report: microsoft/vscode" in response
    assert "Please specify at least 2 repositories" not in response
