#!/usr/bin/env python3
"""
🌟 GitHub AI Brain — Feature Demonstration Script
Executes comprehensive end-to-end demonstrations of repository health analysis,
multi-repo competitive benchmarking, organization auditing, and query processing.
"""

import time
from github_agent import GitHubAIBrain
from multi_repo import MultiRepoAnalyzer


def run_demo():
    """Run full suite demonstration."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║              🤖 GITHUB AI BRAIN DEMONSTRATION                ║
║           Repository Health, Benchmarking & Intelligence     ║
╚══════════════════════════════════════════════════════════════╝
""")

    agent = GitHubAIBrain()
    analyzer = MultiRepoAnalyzer(agent)

    test_scenarios = [
        {
            "title": "1. Repository Health Analysis",
            "query": "What is the health status of microsoft/vscode?",
        },
        {
            "title": "2. Competitive Repository Benchmarking",
            "query": "Compare tensorflow/tensorflow vs pytorch/pytorch",
        },
        {
            "title": "3. Organization-Wide Audit",
            "query": "Analyze organization facebook",
        },
        {
            "title": "4. Recent Commit Activity Tracking",
            "query": "Get recent commits in kubernetes/kubernetes",
        },
        {
            "title": "5. Workflow Status Verification",
            "query": "Check workflow status in pytorch/pytorch",
        },
    ]

    passed_count = 0

    for scenario in test_scenarios:
        print(f"\n📌 {scenario['title']}")
        print(f"   🔍 Query: \"{scenario['query']}\"")
        try:
            response = agent.query(scenario["query"])
            first_line = response.strip().split("\n")[0] if response else "No response"
            print(f"   ✅ Result: Success ({len(response)} characters returned)")
            print(f"   📄 Output Preview: {first_line}")
            passed_count += 1
        except Exception as e:
            print(f"   ❌ Execution Error: {e}")

        time.sleep(1)

    print(f"\n🏆 DEMONSTRATION COMPLETE: {passed_count}/{len(test_scenarios)} scenarios executed successfully.")


if __name__ == "__main__":
    run_demo()
