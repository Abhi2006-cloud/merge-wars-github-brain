#!/usr/bin/env python3
"""
🤖 GitHub AI Brain - Core Agent Implementation
Intelligent repository management, health scoring, and multi-repo analysis.
"""

import os
import re
import time
import json
import csv
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone, timedelta

import requests
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("GitHubAIBrain")


class GitHubAIBrain:
    """AI-powered GitHub repository analysis and intelligence engine."""

    def __init__(self, token: Optional[str] = None):
        self.github_token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-AI-Brain/1.0",
        }
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
        else:
            logger.warning("GITHUB_TOKEN not found. Rate limit is restricted to 60 requests/hour.")

    def _api_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make an authenticated HTTP request to the GitHub REST API.

        Args:
            endpoint: API endpoint path (e.g. 'repos/owner/repo')
            params: Optional query parameters

        Returns:
            Decoded JSON response or error dict.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.get(url, headers=self.headers, params=params or {}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else None
            return {"error": f"HTTP {status_code}: {e.response.reason if e.response is not None else str(e)}", "status_code": status_code}
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": None}

    def get_repository_info(self, repo: str) -> Dict[str, Any]:
        """Get basic metadata for a repository."""
        res = self._api_request(f"repos/{repo}")
        return res if isinstance(res, dict) else {"error": "Invalid response format"}

    def get_issues(self, repo: str, state: str = "open", limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch repository issues (excluding pull requests)."""
        result = self._api_request(f"repos/{repo}/issues", {"state": state, "per_page": limit, "sort": "updated"})
        if isinstance(result, list):
            # GitHub API returns PRs as issues; filter out items containing 'pull_request' key
            return [i for i in result if "pull_request" not in i]
        return []

    def get_pull_requests(self, repo: str, state: str = "open", limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch repository pull requests."""
        result = self._api_request(f"repos/{repo}/pulls", {"state": state, "per_page": limit, "sort": "updated"})
        return result if isinstance(result, list) else []

    def get_commits(self, repo: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch recent repository commits."""
        result = self._api_request(f"repos/{repo}/commits", {"per_page": limit})
        return result if isinstance(result, list) else []

    def get_branches(self, repo: str) -> List[Dict[str, Any]]:
        """Fetch repository branches."""
        result = self._api_request(f"repos/{repo}/branches")
        return result if isinstance(result, list) else []

    def get_workflow_runs(self, repo: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch recent GitHub Actions workflow runs."""
        result = self._api_request(f"repos/{repo}/actions/runs", {"per_page": limit})
        if isinstance(result, dict):
            return result.get("workflow_runs", [])
        return []

    def analyze_repository_health(self, repo: str) -> Dict[str, Any]:
        """Analyze repository health and generate structured metrics.

        Args:
            repo: Repository in 'owner/repo' format

        Returns:
            Dict containing activity metrics, workflow status, and health rating.
        """
        logger.info(f"Analyzing repository health for {repo}...")
        repo_info = self.get_repository_info(repo)

        if "error" in repo_info:
            return {"repository": repo, "error": f"Cannot access repository: {repo_info['error']}"}

        issues = self.get_issues(repo, limit=30)
        prs = self.get_pull_requests(repo, limit=30)
        commits = self.get_commits(repo, limit=30)
        workflows = self.get_workflow_runs(repo, limit=20)

        activity_score = self._calculate_activity_score(commits, issues, prs)
        workflow_summary = self._analyze_workflows(workflows)

        health_rating = "🔴 Needs Attention"
        if activity_score > 80:
            health_rating = "🟢 Excellent"
        elif activity_score > 60:
            health_rating = "🟡 Good"
        elif activity_score > 40:
            health_rating = "🟠 Fair"

        return {
            "repository": repo,
            "description": repo_info.get("description", "No description provided"),
            "last_updated": repo_info.get("updated_at"),
            "stars": repo_info.get("stargazers_count", 0),
            "forks": repo_info.get("forks_count", 0),
            "open_issues": len(issues),
            "open_prs": len(prs),
            "recent_commits": len(commits),
            "workflow_status": workflow_summary,
            "activity_score": activity_score,
            "health_rating": health_rating,
        }

    def _analyze_workflows(self, workflows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze GitHub Actions workflow execution statuses."""
        if not workflows:
            return {"status": "No workflows found", "latest_status": "N/A", "total_runs": 0}

        statuses: Dict[str, int] = {}
        for run in workflows:
            status = run.get("conclusion") or run.get("status") or "unknown"
            statuses[status] = statuses.get(status, 0) + 1

        latest = workflows[0].get("conclusion") or workflows[0].get("status") or "unknown"
        return {
            "total_runs": len(workflows),
            "statuses": statuses,
            "latest_status": latest,
        }

    def _calculate_activity_score(self, commits: List[Dict], issues: List[Dict], prs: List[Dict]) -> int:
        """Calculate weighted activity score (0-100) based on recency of contributions."""
        score = 0

        # Recent commit activity (up to 40 points)
        recent_commits = sum(1 for c in commits if self._is_recent(c.get("commit", {}).get("author", {}).get("date")))
        score += min(recent_commits * 8, 40)

        # Recent issue update activity (up to 30 points)
        recent_issues = sum(1 for i in issues if self._is_recent(i.get("updated_at")))
        score += min(recent_issues * 3, 30)

        # Recent PR update activity (up to 30 points)
        recent_prs = sum(1 for pr in prs if self._is_recent(pr.get("updated_at")))
        score += min(recent_prs * 5, 30)

        return min(score, 100)

    def _is_recent(self, date_str: Optional[str], days: int = 30) -> bool:
        """Check whether an ISO timestamp string falls within the past N days."""
        if not date_str:
            return False
        try:
            # Handle ISO string with trailing Z or timezone offset
            clean_str = date_str.replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean_str)
            now = datetime.now(dt.tzinfo or timezone.utc)
            return (now - dt) <= timedelta(days=days)
        except (ValueError, TypeError):
            return False

    def compare_repositories(self, repos: List[str]) -> Dict[str, Any]:
        """Compare multiple repositories side-by-side."""
        logger.info(f"Comparing {len(repos)} repositories...")
        comparisons = {}

        for repo in repos:
            comparisons[repo] = self.analyze_repository_health(repo)
            time.sleep(0.5)

        ranked = sorted(
            comparisons.items(),
            key=lambda item: item[1].get("activity_score", 0) if "error" not in item[1] else -1,
            reverse=True,
        )

        return {
            "comparison_date": datetime.now(timezone.utc).isoformat(),
            "repositories_analyzed": len(repos),
            "detailed_analysis": comparisons,
            "ranking": [repo for repo, _ in ranked],
        }

    def query(self, question: str) -> str:
        """Process natural language user requests and return formatted markdown answers."""
        q = question.strip().lower()
        repo = self._extract_repository(question)

        # Organization analysis query
        if "org" in q or "organization" in q:
            org = self._extract_org_name(question)
            if org:
                from multi_repo import MultiRepoAnalyzer
                analyzer = MultiRepoAnalyzer(self)
                res = analyzer.organization_analysis(org)
                return analyzer.format_org_report(res)
            return "❌ Please specify an organization name (e.g., 'Analyze organization facebook')"

        # Compare repositories query
        if "compare" in q or re.search(r"\bvs\b", q):
            repos = self._extract_multiple_repositories(question)
            if len(repos) >= 2:
                comparison = self.compare_repositories(repos)
                return self._format_comparison_response(comparison)
            return "❌ Please specify at least 2 repositories to compare (e.g., 'Compare tensorflow/tensorflow vs pytorch/pytorch')"

        # Repository health analysis query
        if "health" in q or "analyze" in q or "status" in q:
            if repo:
                analysis = self.analyze_repository_health(repo)
                return self._format_health_response(analysis)
            return "❌ Please specify a repository in 'owner/repo' format (e.g., 'microsoft/vscode')"

        # Issues query
        if "issue" in q:
            if repo:
                issues = self.get_issues(repo)
                return self._format_issues_response(repo, issues)
            return "❌ Please specify a repository for issue queries."

        # PR query
        if "pull request" in q or "pr" in q:
            if repo:
                prs = self.get_pull_requests(repo)
                return self._format_prs_response(repo, prs)
            return "❌ Please specify a repository for pull request queries."

        # Commits query
        if "commit" in q:
            if repo:
                commits = self.get_commits(repo)
                return self._format_commits_response(repo, commits)
            return "❌ Please specify a repository for commit queries."

        # Workflows query
        if "workflow" in q or "action" in q:
            if repo:
                workflows = self.get_workflow_runs(repo)
                return self._format_workflows_response(repo, workflows)
            return "❌ Please specify a repository for workflow queries."

        # Fallback helper response
        return self._get_help_response()

    def _extract_repository(self, text: str) -> Optional[str]:
        """Extract 'owner/repo' pattern from text."""
        match = re.search(r"([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)", text)
        return match.group(1) if match else None

    def _extract_multiple_repositories(self, text: str) -> List[str]:
        """Extract all unique 'owner/repo' patterns from text."""
        matches = re.findall(r"([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)", text)
        return list(dict.fromkeys(matches))

    def _extract_org_name(self, text: str) -> Optional[str]:
        """Extract organization handle from query."""
        match = re.search(r"(?:org|organization)\s+([a-zA-Z0-9_.-]+)", text, re.IGNORECASE)
        if match:
            return match.group(1)
        # Fallback if query is e.g. "analyze facebook org"
        match_alt = re.search(r"([a-zA-Z0-9_.-]+)\s+(?:org|organization)", text, re.IGNORECASE)
        return match_alt.group(1) if match_alt else None

    def _format_health_response(self, analysis: Dict[str, Any]) -> str:
        """Format health audit into a clean markdown string."""
        if "error" in analysis:
            return f"❌ Error: {analysis['error']}"

        wf = analysis.get("workflow_status", {})
        return f"""🏥 **Repository Health Report: {analysis['repository']}**

📝 **Description:** {analysis.get('description', 'N/A')}

📊 **Key Metrics:**
   ⭐ Stars: {analysis['stars']:,}
   🍴 Forks: {analysis['forks']:,}
   📝 Open Issues: {analysis['open_issues']}
   🔄 Open Pull Requests: {analysis['open_prs']}
   💻 Recent Commits: {analysis['recent_commits']}

📈 **Health Rating:** {analysis['health_rating']}
🎯 **Activity Score:** {analysis['activity_score']}/100
⚙️ **Latest Workflow Status:** {wf.get('latest_status', 'N/A')}
📅 **Last Updated:** {analysis.get('last_updated', 'N/A')}
"""

    def _format_comparison_response(self, comparison: Dict[str, Any]) -> str:
        """Format competitive repo benchmarking into a clean markdown string."""
        response = f"🔍 **Repository Benchmarking Report** ({comparison['repositories_analyzed']} repos analyzed)\n\n"
        for i, repo in enumerate(comparison["ranking"], 1):
            data = comparison["detailed_analysis"][repo]
            if "error" not in data:
                response += (
                    f"{i}. **{repo}** — Rating: {data['health_rating']} | "
                    f"Score: {data['activity_score']}/100 | "
                    f"⭐ {data['stars']:,}\n"
                )
            else:
                response += f"{i}. **{repo}** — ❌ Access Error\n"
        return response

    def _format_issues_response(self, repo: str, issues: List[Dict[str, Any]]) -> str:
        """Format issue list into markdown."""
        if not issues:
            return f"📝 No open issues found for **{repo}**."
        resp = f"📝 **Open Issues in {repo}** (Showing top {min(len(issues), 5)})\n\n"
        for issue in issues[:5]:
            resp += f"• **#{issue['number']}**: {issue['title'][:70]}\n"
        return resp

    def _format_prs_response(self, repo: str, prs: List[Dict[str, Any]]) -> str:
        """Format PR list into markdown."""
        if not prs:
            return f"🔄 No open pull requests found for **{repo}**."
        resp = f"🔄 **Open Pull Requests in {repo}** (Showing top {min(len(prs), 5)})\n\n"
        for pr in prs[:5]:
            resp += f"• **#{pr['number']}**: {pr['title'][:70]}\n"
        return resp

    def _format_commits_response(self, repo: str, commits: List[Dict[str, Any]]) -> str:
        """Format commit history into markdown."""
        if not commits:
            return f"💻 No recent commits found for **{repo}**."
        resp = f"💻 **Recent Commits in {repo}** (Showing top {min(len(commits), 5)})\n\n"
        for c in commits[:5]:
            msg = c.get("commit", {}).get("message", "").split("\n")[0][:70]
            sha = c.get("sha", "")[:7]
            resp += f"• `{sha}`: {msg}\n"
        return resp

    def _format_workflows_response(self, repo: str, workflows: List[Dict[str, Any]]) -> str:
        """Format workflow runs into markdown."""
        if not workflows:
            return f"⚙️ No GitHub Actions workflow runs found for **{repo}**."
        resp = f"⚙️ **Workflow Runs in {repo}** (Showing top {min(len(workflows), 5)})\n\n"
        for run in workflows[:5]:
            status = run.get("conclusion") or run.get("status") or "unknown"
            name = run.get("name", "Workflow")
            resp += f"• **{name}**: {status} (Run #{run.get('run_number', 'N/A')})\n"
        return resp

    def _get_help_response(self) -> str:
        """Provide structured usage instructions."""
        return """🤖 **GitHub AI Brain - Help & Command Reference**

Supported Queries:
• **Repository Health**: `"Analyze microsoft/vscode"`
• **Competitive Comparison**: `"Compare tensorflow/tensorflow vs pytorch/pytorch"`
• **Organization Audit**: `"Analyze organization facebook"`
• **Issue Audit**: `"Show open issues in facebook/react"`
• **Pull Requests**: `"List PRs in kubernetes/kubernetes"`
• **Recent Commits**: `"Show commits in microsoft/vscode"`
• **Workflow Status**: `"Check workflows in pytorch/pytorch"`

💡 *Note: Always use 'owner/repo' format for individual repository queries.*
"""

    def export_report_json(self, data: Dict[str, Any], filepath: str) -> str:
        """Export report dictionary to a JSON file.

        Args:
            data: Data dictionary to export
            filepath: Destination file path

        Returns:
            Path of written JSON file.
        """
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Report exported to JSON: {filepath}")
        return filepath

    def export_report_csv(self, data: Dict[str, Any], filepath: str) -> str:
        """Export analysis metrics to a flat CSV file.

        Args:
            data: Health analysis or organization audit dictionary
            filepath: Destination file path

        Returns:
            Path of written CSV file.
        """
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if "top_repositories" in data:
                # Organization audit report format
                writer.writerow(["Repository", "Health Rating", "Activity Score", "Stars", "Forks", "Open Issues"])
                for repo in data.get("top_repositories", []):
                    writer.writerow([
                        repo.get("repository"),
                        repo.get("health_rating"),
                        repo.get("activity_score"),
                        repo.get("stars"),
                        repo.get("forks"),
                        repo.get("open_issues"),
                    ])
            elif "repository" in data:
                # Single repository report format
                writer.writerow(["Metric", "Value"])
                writer.writerow(["Repository", data.get("repository")])
                writer.writerow(["Description", data.get("description")])
                writer.writerow(["Health Rating", data.get("health_rating")])
                writer.writerow(["Activity Score", data.get("activity_score")])
                writer.writerow(["Stars", data.get("stars")])
                writer.writerow(["Forks", data.get("forks")])
                writer.writerow(["Open Issues", data.get("open_issues")])
                writer.writerow(["Open PRs", data.get("open_prs")])
                writer.writerow(["Recent Commits", data.get("recent_commits")])
                writer.writerow(["Last Updated", data.get("last_updated")])
            else:
                # Generic dictionary key-value output
                writer.writerow(["Key", "Value"])
                for k, v in data.items():
                    writer.writerow([k, str(v)])

        logger.info(f"Report exported to CSV: {filepath}")
        return filepath

