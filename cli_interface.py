#!/usr/bin/env python3
"""
💻 GitHub AI Brain - Interactive CLI Interface
Terminal user interface for interactive repository intelligence and management.
"""

import os
import sys
from typing import List
from github_agent import GitHubAIBrain
from multi_repo import MultiRepoAnalyzer


class GitHubCLI:
    """Interactive command-line interface for GitHub AI Brain."""

    def __init__(self):
        self.agent = GitHubAIBrain()
        self.multi_analyzer = MultiRepoAnalyzer(self.agent)
        self.running = True

    def run(self):
        """Start the interactive CLI loop."""
        self.show_welcome()

        while self.running:
            try:
                user_input = input("\n[GitHub AI Brain] > ").strip()

                if not user_input:
                    continue

                cmd = user_input.lower()
                if cmd in ["exit", "quit", "q"]:
                    self.running = False
                    print("\nGoodbye! May your repositories remain healthy and build green! 🚀")
                    break
                elif cmd in ["help", "h", "?"]:
                    self.show_help()
                    continue
                elif cmd in ["clear", "cls"]:
                    os.system("clear" if os.name == "posix" else "cls")
                    continue
                elif cmd.startswith("demo"):
                    self.run_demo()
                    continue

                print("\nProcessing request...")
                response = self.agent.query(user_input)
                print(f"\n{response}")

            except KeyboardInterrupt:
                print("\n\nSession interrupted. Type 'exit' to quit.")
                continue
            except Exception as e:
                print(f"\n❌ Error processing query: {e}")
                continue

    def show_welcome(self):
        """Display ASCII header banner and authentication notice."""
        print("""
================================================================
           🤖 GITHUB AI BRAIN — REPOSITORY INTELLIGENCE          
================================================================

An intelligent companion for repository metrics, activity scoring,
workflow tracking, and organization-wide benchmarking.

Type 'help' for command reference
Type 'demo' for example queries
Type 'exit' to quit
""")

        if not os.getenv("GITHUB_TOKEN") and not os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
            print("""
⚠️  NOTICE: No GitHub Token Detected
   • Operating under unauthenticated rate limits (60 req/hour).
   • Set GITHUB_TOKEN in your environment or .env file for 5,000 req/hour.
""")
        else:
            print("🔑 GitHub Token Authenticated — 5,000 requests/hour limit active.")

    def show_help(self):
        """Display help guidance."""
        print("""
📖 GITHUB AI BRAIN COMMAND REFERENCE

Natural Language Query Examples:
   • "Analyze microsoft/vscode repository"
   • "Compare tensorflow/tensorflow vs pytorch/pytorch"
   • "Analyze organization facebook"
   • "Show open issues in facebook/react"
   • "List pull requests in kubernetes/kubernetes"
   • "Get recent commits from tensorflow/tensorflow"
   • "Check workflow status in pytorch/pytorch"

Built-In Shell Commands:
   • help, h, ?     - Show this help summary
   • demo           - Run interactive demo queries
   • clear, cls     - Clear terminal window
   • exit, quit, q  - Exit CLI session

Repository Format:
   Always specify repos as 'owner/repo' (e.g., 'microsoft/vscode').
""")

    def run_demo(self):
        """Run interactive demonstration sequence."""
        demo_queries = [
            "Analyze microsoft/vscode repository",
            "Show open issues in facebook/react",
            "List pull requests in kubernetes/kubernetes",
            "Get recent commits from tensorflow/tensorflow",
            "Compare tensorflow/tensorflow vs pytorch/pytorch",
            "Analyze organization facebook",
        ]

        print("\n🎬 DEMO MODE — Available Queries:\n")
        for i, query in enumerate(demo_queries, 1):
            print(f"  {i}. \"{query}\"")

        try:
            choice = input("\nSelect a query number (1-6) or press Enter to skip: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(demo_queries):
                selected = demo_queries[int(choice) - 1]
                print(f"\nRunning: \"{selected}\"")
                print("Processing...")
                response = self.agent.query(selected)
                print(f"\n{response}")
            else:
                print("\nDemo mode exited. Ready for queries!")
        except (ValueError, KeyboardInterrupt):
            print("\nDemo skipped.")


def main():
    """Main CLI entry point."""
    try:
        cli = GitHubCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error starting CLI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
