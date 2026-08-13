#!/usr/bin/env python3
"""
💻 GitHub AI Brain - Interactive & Command-Line Interface
Terminal user interface and CLI options for repository intelligence and analytics.
"""

import os
import sys
import argparse
from typing import List, Optional
from github_agent import GitHubAIBrain
from multi_repo import MultiRepoAnalyzer


class GitHubCLI:
    """Command-line interface supporting interactive REPL and flag-based execution."""

    def __init__(self):
        self.agent = GitHubAIBrain()
        self.multi_analyzer = MultiRepoAnalyzer(self.agent)
        self.running = True

    def run(self, args: Optional[List[str]] = None):
        """Start CLI execution, routing to non-interactive mode or REPL based on flags."""
        parser = argparse.ArgumentParser(
            description="🤖 GitHub AI Brain — Repository Intelligence & Analytics Engine",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""Examples:
  python3 main.py --analyze microsoft/vscode
  python3 main.py --compare tensorflow/tensorflow pytorch/pytorch
  python3 main.py --org facebook --export json --out report.json
  python3 main.py --query "Show open issues in facebook/react"
""",
        )

        parser.add_argument("-v", "--version", action="version", version="GitHub AI Brain v1.0.0")
        parser.add_argument("-a", "--analyze", type=str, metavar="REPO", help="Analyze repository health (e.g., 'owner/repo')")
        parser.add_argument("-c", "--compare", nargs="+", metavar="REPO", help="Compare multiple repositories side-by-side")
        parser.add_argument("-o", "--org", type=str, metavar="ORG", help="Perform organization health audit")
        parser.add_argument("-q", "--query", type=str, metavar="QUERY", help="Execute natural language terminal query")
        parser.add_argument("-e", "--export", type=str, choices=["json", "csv"], help="Export audit results (json or csv)")
        parser.add_argument("--out", type=str, help="Destination filepath for export output")

        parsed_args = parser.parse_args(args)

        # Non-interactive CLI flag execution
        if parsed_args.analyze:
            self._handle_analyze_flag(parsed_args.analyze, parsed_args.export, parsed_args.out)
            return

        if parsed_args.compare:
            self._handle_compare_flag(parsed_args.compare, parsed_args.export, parsed_args.out)
            return

        if parsed_args.org:
            self._handle_org_flag(parsed_args.org, parsed_args.export, parsed_args.out)
            return

        if parsed_args.query:
            response = self.agent.query(parsed_args.query)
            print(f"\n{response}")
            return

        # Interactive REPL mode (default when no flags passed)
        self.run_repl()

    def run_repl(self):
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

    def _handle_analyze_flag(self, repo: str, export_fmt: Optional[str], outfile: Optional[str]):
        """Handle --analyze command line flag."""
        print(f"\n🔍 Analyzing repository: {repo}...")
        report = self.agent.analyze_repository_health(repo)
        print(f"\n{self.agent._format_health_response(report)}")

        if export_fmt:
            filepath = outfile or f"{repo.replace('/', '_')}_health.{export_fmt}"
            if export_fmt == "csv":
                self.agent.export_report_csv(report, filepath)
            else:
                self.agent.export_report_json(report, filepath)
            print(f"📁 Report saved to {filepath}")

    def _handle_compare_flag(self, repos: List[str], export_fmt: Optional[str], outfile: Optional[str]):
        """Handle --compare command line flag."""
        if len(repos) < 2:
            print("❌ Please specify at least 2 repositories to compare.")
            return
        print(f"\n🔍 Benchmarking repositories: {', '.join(repos)}...")
        comp = self.agent.compare_repositories(repos)
        print(f"\n{self.agent._format_comparison_response(comp)}")

        if export_fmt:
            filepath = outfile or f"repo_comparison.{export_fmt}"
            if export_fmt == "csv":
                self.agent.export_report_csv(comp, filepath)
            else:
                self.agent.export_report_json(comp, filepath)
            print(f"📁 Comparison report saved to {filepath}")

    def _handle_org_flag(self, org: str, export_fmt: Optional[str], outfile: Optional[str]):
        """Handle --org command line flag."""
        print(f"\n🏢 Auditing organization: {org}...")
        report = self.multi_analyzer.organization_analysis(org)
        print(f"\n{self.multi_analyzer.format_org_report(report)}")

        if export_fmt:
            filepath = outfile or f"{org}_org_audit.{export_fmt}"
            self.multi_analyzer.export_org_report(report, filepath, fmt=export_fmt)
            print(f"📁 Organization audit exported to {filepath}")

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

Command-Line Flag Examples:
   • python3 main.py --analyze microsoft/vscode
   • python3 main.py --compare tensorflow/tensorflow pytorch/pytorch
   • python3 main.py --org facebook --export json --out facebook_report.json

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
