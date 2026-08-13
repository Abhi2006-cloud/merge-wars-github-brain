#!/usr/bin/env python3
"""
📊 GitHub Multi-Repository & Organization Analyzer
Provides organization-wide repository audits and competitive benchmarking.
"""

import time
from typing import Dict, List, Any, Optional
from github_agent import GitHubAIBrain


class MultiRepoAnalyzer:
    """Organization-level and cross-repository competitive analysis engine."""

    def __init__(self, agent: Optional[GitHubAIBrain] = None):
        self.agent = agent or GitHubAIBrain()

    def organization_analysis(self, org_name: str, max_repos: int = 3) -> Dict[str, Any]:
        """Analyze public repositories across an entire GitHub organization.

        Args:
            org_name: GitHub organization handle (e.g., 'facebook', 'microsoft')
            max_repos: Maximum number of repositories to evaluate

        Returns:
            Dict containing org metrics, top repositories, and aggregated health scores.
        """
        print(f"🔍 Fetching organization repositories for '{org_name}'...")
        endpoint = f"orgs/{org_name}/repos"
        repos_data = self.agent._api_request(endpoint, {"per_page": max_repos, "sort": "pushed"})

        if isinstance(repos_data, dict) and "error" in repos_data:
            return {"error": f"Failed to access organization '{org_name}': {repos_data['error']}"}

        if not isinstance(repos_data, list) or not repos_data:
            return {"error": f"No public repositories found for organization '{org_name}'."}

        analyzed_repos = []
        total_stars = 0
        total_forks = 0
        total_open_issues = 0

        for repo_info in repos_data[:max_repos]:
            repo_full_name = repo_info.get("full_name")
            if not repo_full_name:
                continue

            health = self.agent.analyze_repository_health(repo_full_name)
            if "error" not in health:
                total_stars += health.get("stars", 0)
                total_forks += health.get("forks", 0)
                total_open_issues += health.get("open_issues", 0)
                analyzed_repos.append(health)

            time.sleep(0.5)  # Rate limiting safety pause

        # Sort repos by activity score descending
        analyzed_repos.sort(key=lambda r: r.get("activity_score", 0), reverse=True)

        avg_score = (
            sum(r.get("activity_score", 0) for r in analyzed_repos) / len(analyzed_repos)
            if analyzed_repos
            else 0
        )

        return {
            "organization": org_name,
            "repositories_analyzed": len(analyzed_repos),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "total_open_issues": total_open_issues,
            "average_activity_score": round(avg_score, 1),
            "top_repositories": analyzed_repos,
        }

    def competitive_analysis(self, repo_list: List[str]) -> Dict[str, Any]:
        """Perform side-by-side competitive benchmarking across multiple repositories.

        Args:
            repo_list: List of repo identifiers in 'owner/repo' format

        Returns:
            Dict containing detailed comparisons and head-to-head ranking.
        """
        return self.agent.compare_repositories(repo_list)

    def format_org_report(self, report: Dict[str, Any]) -> str:
        """Format organization analysis output as a structured Markdown report."""
        if "error" in report:
            return f"❌ Error: {report['error']}"

        output = f"""
🏢 **Organization Health Audit: {report['organization']}**

📊 **Aggregated Metrics:**
   • Repositories Analyzed: {report['repositories_analyzed']}
   • Total Stars: {report['total_stars']:,}
   • Total Forks: {report['total_forks']:,}
   • Open Issues across repos: {report['total_open_issues']:,}
   • Average Activity Score: {report['average_activity_score']}/100

🏆 **Top Repositories by Activity:**
"""
        for i, repo in enumerate(report["top_repositories"][:5], 1):
            output += (
                f"   {i}. **{repo['repository']}** | "
                f"{repo['health_rating']} | "
                f"Score: {repo['activity_score']}/100 | "
                f"⭐ {repo['stars']:,}\n"
            )

        return output


if __name__ == "__main__":
    analyzer = MultiRepoAnalyzer()
    print("Testing MultiRepoAnalyzer...")
    result = analyzer.organization_analysis("github", max_repos=3)
    print(analyzer.format_org_report(result))
