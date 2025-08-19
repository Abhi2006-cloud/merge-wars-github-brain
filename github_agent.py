#!/usr/bin/env python3
"""
🤖 GitHub AI Brain - Core Agent Implementation
Intelligent repository management and analysis using MCP
"""

import os
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    print("❌ requests not installed. Installing...")
    os.system("pip install requests")
    import requests

class GitHubAIBrain:
    """AI-powered GitHub repository analysis and management"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'token {self.github_token}' if self.github_token else None,
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-AI-Brain/1.0'
        }
        
        if not self.github_token:
            print("⚠️  GITHUB_TOKEN not found. API rate limits will apply.")
            print("   Set GITHUB_TOKEN environment variable for full functionality.")
    
    def _api_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make authenticated GitHub API request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.get(url, headers=self.headers, params=params or {})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def get_repository_info(self, repo: str) -> Dict:
        """Get basic repository information"""
        return self._api_request(f'repos/{repo}')
    
    def get_issues(self, repo: str, state: str = 'open', limit: int = 10) -> List[Dict]:
        """Get repository issues"""
        result = self._api_request(f'repos/{repo}/issues', {
            'state': state,
            'per_page': limit,
            'sort': 'updated'
        })
        return result if isinstance(result, list) else []
    
    def get_pull_requests(self, repo: str, state: str = 'open', limit: int = 10) -> List[Dict]:
        """Get repository pull requests"""
        result = self._api_request(f'repos/{repo}/pulls', {
            'state': state,
            'per_page': limit,
            'sort': 'updated'
        })
        return result if isinstance(result, list) else []
    
    def get_commits(self, repo: str, limit: int = 10) -> List[Dict]:
        """Get recent commits"""
        result = self._api_request(f'repos/{repo}/commits', {
            'per_page': limit
        })
        return result if isinstance(result, list) else []
    
    def get_branches(self, repo: str) -> List[Dict]:
        """Get repository branches"""
        result = self._api_request(f'repos/{repo}/branches')
        return result if isinstance(result, list) else []
    
    def get_workflow_runs(self, repo: str, limit: int = 10) -> List[Dict]:
        """Get GitHub Actions workflow runs"""
        result = self._api_request(f'repos/{repo}/actions/runs', {
            'per_page': limit
        })
        return result.get('workflow_runs', []) if isinstance(result, dict) else []
    
    def analyze_repository_health(self, repo: str) -> Dict:
        """Analyze repository health and provide insights"""
        print(f"🔍 Analyzing repository health for {repo}...")
        
        repo_info = self.get_repository_info(repo)
        if 'error' in repo_info:
            return {"error": f"Cannot access repository: {repo_info['error']}"}
        
        issues = self.get_issues(repo, limit=50)
        prs = self.get_pull_requests(repo, limit=50)
        commits = self.get_commits(repo, limit=50)
        workflows = self.get_workflow_runs(repo, limit=20)
        
        # Calculate health metrics
        analysis = {
            "repository": repo,
            "last_updated": repo_info.get('updated_at'),
            "stars": repo_info.get('stargazers_count', 0),
            "forks": repo_info.get('forks_count', 0),
            "open_issues": len(issues),
            "open_prs": len(prs),
            "recent_commits": len(commits),
            "workflow_status": self._analyze_workflows(workflows),
            "activity_score": self._calculate_activity_score(commits, issues, prs),
            "health_rating": "Unknown"
        }
        
        # Determine health rating
        score = analysis["activity_score"]
        if score > 80:
            analysis["health_rating"] = "🟢 Excellent"
        elif score > 60:
            analysis["health_rating"] = "🟡 Good"
        elif score > 40:
            analysis["health_rating"] = "🟠 Fair"
        else:
            analysis["health_rating"] = "🔴 Needs Attention"
        
        return analysis
    
    def _analyze_workflows(self, workflows: List[Dict]) -> Dict:
        """Analyze workflow run status"""
        if not workflows:
            return {"status": "No workflows found"}
        
        statuses = {}
        for run in workflows:
            status = run.get('conclusion', run.get('status', 'unknown'))
            statuses[status] = statuses.get(status, 0) + 1
        
        return {
            "total_runs": len(workflows),
            "statuses": statuses,
            "latest_status": workflows[0].get('conclusion', 'unknown') if workflows else 'none'
        }
    
    def _calculate_activity_score(self, commits: List, issues: List, prs: List) -> int:
        """Calculate repository activity score (0-100)"""
        score = 0
        
        # Recent commits (40 points max)
        if commits:
            recent_commits = len([c for c in commits if self._is_recent(c.get('commit', {}).get('author', {}).get('date'))])
            score += min(recent_commits * 8, 40)
        
        # Issue activity (30 points max)
        if issues:
            recent_issues = len([i for i in issues if self._is_recent(i.get('updated_at'))])
            score += min(recent_issues * 3, 30)
        
        # PR activity (30 points max)
        if prs:
            recent_prs = len([pr for pr in prs if self._is_recent(pr.get('updated_at'))])
            score += min(recent_prs * 5, 30)
        
        return min(score, 100)
    
    def _is_recent(self, date_str: Optional[str], days: int = 30) -> bool:
        """Check if date is within recent days"""
        if not date_str:
            return False
        
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return (datetime.now(date.tzinfo) - date).days <= days
        except (ValueError, TypeError):
            return False
    
    def compare_repositories(self, repos: List[str]) -> Dict:
        """Compare multiple repositories"""
        print(f"🔍 Comparing {len(repos)} repositories...")
        
        comparisons = {}
        for repo in repos:
            print(f"   Analyzing {repo}...")
            comparisons[repo] = self.analyze_repository_health(repo)
            time.sleep(1)  # Rate limiting
        
        # Rank repositories
        ranked = sorted(
            comparisons.items(),
            key=lambda x: x[1].get('activity_score', 0) if isinstance(x[1], dict) and 'error' not in x[1] else 0,
            reverse=True
        )
        
        return {
            "comparison_date": datetime.now().isoformat(),
            "repositories_analyzed": len(repos),
            "detailed_analysis": comparisons,
            "ranking": [repo for repo, _ in ranked]
        }
    
    def query(self, question: str) -> str:
        """Process natural language queries about repositories"""
        question_lower = question.lower()
        
        # Extract repository from query
        repo = self._extract_repository(question)
        
        if "health" in question_lower or "analyze" in question_lower:
            if repo:
                analysis = self.analyze_repository_health(repo)
                return self._format_health_response(analysis)
            else:
                return "❌ Please specify a repository (format: owner/repo)"
        
        elif "compare" in question_lower:
            repos = self._extract_multiple_repositories(question)
            if len(repos) >= 2:
                comparison = self.compare_repositories(repos)
                return self._format_comparison_response(comparison)
            else:
                return "❌ Please specify at least 2 repositories to compare"
        
        elif "issues" in question_lower:
            if repo:
                issues = self.get_issues(repo)
                return self._format_issues_response(repo, issues)
            else:
                return "❌ Please specify a repository for issues"
        
        elif "pull request" in question_lower or "pr" in question_lower:
            if repo:
                prs = self.get_pull_requests(repo)
                return self._format_prs_response(repo, prs)
            else:
                return "❌ Please specify a repository for pull requests"
        
        elif "commit" in question_lower:
            if repo:
                commits = self.get_commits(repo)
                return self._format_commits_response(repo, commits)
            else:
                return "❌ Please specify a repository for commits"
        
        elif "workflow" in question_lower or "action" in question_lower:
            if repo:
                workflows = self.get_workflow_runs(repo)
                return self._format_workflows_response(repo, workflows)
            else:
                return "❌ Please specify a repository for workflows"
        
        else:
            return self._get_help_response()
    
    def _extract_repository(self, text: str) -> Optional[str]:
        """Extract repository name from text"""
        import re
        # Look for owner/repo pattern
        match = re.search(r'([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)', text)
        return match.group(1) if match else None
    
    def _extract_multiple_repositories(self, text: str) -> List[str]:
        """Extract multiple repository names from text"""
        import re
        matches = re.findall(r'([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)', text)
        return list(set(matches))  # Remove duplicates
    
    def _format_health_response(self, analysis: Dict) -> str:
        """Format repository health analysis response"""
        if 'error' in analysis:
            return f"❌ Error: {analysis['error']}"
        
        return f"""
🏥 **Repository Health Report: {analysis['repository']}**

📊 **Overview:**
   ⭐ Stars: {analysis['stars']:,}
   🍴 Forks: {analysis['forks']:,}
   📝 Open Issues: {analysis['open_issues']}
   🔄 Open PRs: {analysis['open_prs']}
   💻 Recent Commits: {analysis['recent_commits']}

📈 **Health Rating:** {analysis['health_rating']}
🎯 **Activity Score:** {analysis['activity_score']}/100

🔧 **Workflow Status:** {analysis['workflow_status'].get('latest_status', 'N/A')}
📅 **Last Updated:** {analysis['last_updated']}
"""
    
    def _format_comparison_response(self, comparison: Dict) -> str:
        """Format repository comparison response"""
        response = f"🔍 **Repository Comparison** ({comparison['repositories_analyzed']} repos)\n\n"
        
        for i, repo in enumerate(comparison['ranking'][:5], 1):
            analysis = comparison['detailed_analysis'][repo]
            if 'error' not in analysis:
                response += f"{i}. **{repo}** - {analysis['health_rating']} (Score: {analysis['activity_score']}/100)\n"
        
        return response
    
    def _format_issues_response(self, repo: str, issues: List[Dict]) -> str:
        """Format issues response"""
        if not issues:
            return f"📝 No open issues found in {repo}"
        
        response = f"📝 **Open Issues in {repo}** ({len(issues)} found)\n\n"
        for issue in issues[:5]:
            response += f"• #{issue['number']}: {issue['title'][:60]}...\n"
        
        return response
    
    def _format_prs_response(self, repo: str, prs: List[Dict]) -> str:
        """Format pull requests response"""
        if not prs:
            return f"🔄 No open pull requests found in {repo}"
        
        response = f"🔄 **Pull Requests in {repo}** ({len(prs)} found)\n\n"
        for pr in prs[:5]:
            response += f"• #{pr['number']}: {pr['title'][:60]}...\n"
        
        return response
    
    def _format_commits_response(self, repo: str, commits: List[Dict]) -> str:
        """Format commits response"""
        if not commits:
            return f"💻 No recent commits found in {repo}"
        
        response = f"💻 **Recent Commits in {repo}** ({len(commits)} found)\n\n"
        for commit in commits[:5]:
            message = commit['commit']['message'].split('\n')[0][:60]
            response += f"• {commit['sha'][:7]}: {message}...\n"
        
        return response
    
    def _format_workflows_response(self, repo: str, workflows: List[Dict]) -> str:
        """Format workflows response"""
        if not workflows:
            return f"⚙️ No workflow runs found in {repo}"
        
        response = f"⚙️ **Workflow Runs in {repo}** ({len(workflows)} found)\n\n"
        for run in workflows[:5]:
            status = run.get('conclusion', run.get('status', 'unknown'))
            response += f"• {run['name']}: {status} ({run.get('created_at', '')[:10]})\n"
        
        return response
    
    def _get_help_response(self) -> str:
        """Get help response for unknown queries"""
        return """
🤖 **GitHub AI Brain Help**

I can help you with:
• Repository health analysis: "Analyze microsoft/vscode"
• Compare repositories: "Compare tensorflow/tensorflow vs pytorch/pytorch"
• List issues: "Show issues in facebook/react"
• Pull requests: "Show PRs in kubernetes/kubernetes"
• Recent commits: "Show commits in microsoft/vscode"
• Workflow status: "Check workflows in pytorch/pytorch"

Just mention the repository in owner/repo format!
"""
