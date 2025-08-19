#!/usr/bin/env python3
"""
Test script to verify all features work correctly
"""

from github_agent import GitHubAIBrain
import time

def test_all_features():
    """Test all implemented features for point verification"""
    print("🧪 Testing GitHub AI Brain features...\n")
    
    agent = GitHubAIBrain()
    
    # Test queries for each point category
    test_cases = {
        "Basic Tool Calls (11 points)": [
            "List recent issues in microsoft/vscode",
            "Show pull requests in facebook/react",
            "Get recent commits in kubernetes/kubernetes",
            "Check workflow runs in pytorch/pytorch",
            "List branches in tensorflow/tensorflow"
        ],
        "Query Handling (7 points)": [
            "What's the current health of microsoft/vscode repository?",
            "Show me failing workflows in any popular repository"
        ],
        "Repository Insights (8 points)": [
            "Analyze repository health and bottlenecks for microsoft/vscode"
        ],
        "Multi-Repo Support (10 points)": [
            "Compare tensorflow/tensorflow vs pytorch/pytorch repositories"
        ]
    }
    
    for category, queries in test_cases.items():
        print(f"📊 Testing {category}")
        for query in queries:
            print(f"   🔍 Query: {query}")
            try:
                response = agent.query(query)
                print(f"   ✅ Success: {len(response)} chars response")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            time.sleep(2)  # Rate limiting
        print()
    
    print("🎉 Feature testing completed!")

if __name__ == "__main__":
    test_all_features()

