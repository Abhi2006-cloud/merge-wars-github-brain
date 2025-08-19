#!/usr/bin/env python3
"""
🌌 Merge Wars: GitHub AI Brain
An intelligent AI companion for repository management using MCP
"""

from cli_interface import GitHubCLI

def main():
    """Main entry point for GitHub AI Brain"""
    cli = GitHubCLI()
    cli.run()

if __name__ == "__main__":
    main()
