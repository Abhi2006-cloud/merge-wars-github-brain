#!/usr/bin/env python3
"""
🌌 Merge Wars: GitHub AI Brain
An intelligent AI companion for repository intelligence, activity scoring, and organization benchmarking.
"""

import sys
from cli_interface import GitHubCLI


def main():
    """Main entry point for GitHub AI Brain CLI & interactive REPL."""
    cli = GitHubCLI()
    cli.run(sys.argv[1:])


if __name__ == "__main__":
    main()
