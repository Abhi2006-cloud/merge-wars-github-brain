#!/usr/bin/env python3
"""
GitHub AI Brain - Interactive CLI Interface
Command-line interface for repository management
"""

import os
import sys
from typing import List, Dict
from github_agent import GitHubAIBrain

class GitHubCLI:
    """Interactive command-line interface for GitHub AI Brain"""
    
    def __init__(self):
        self.agent = GitHubAIBrain()
        self.running = True
        
    def run(self):
        """Start the interactive CLI session"""
        self.show_welcome()
        
        while self.running:
            try:
                user_input = input("\n[GitHub AI Brain] > ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    self.running = False
                    print("Goodbye! May your repositories be ever healthy!")
                    break
                elif user_input.lower() in ['help', 'h', '?']:
                    self.show_help()
                    continue
                elif user_input.lower() in ['clear', 'cls']:
                    os.system('clear' if os.name == 'posix' else 'cls')
                    continue
                elif user_input.lower().startswith('demo'):
                    self.run_demo()
                    continue
                
                # Process query through AI agent
                print("\nProcessing your request...")
                response = self.agent.query(user_input)
                print(f"\n{response}")
                
            except KeyboardInterrupt:
                print("\n\nInterrupted. Use 'exit' to quit properly.")
                continue
            except Exception as e:
                print(f"\nError: {e}")
                continue
    
    def show_welcome(self):
        """Display welcome message"""
        print("""
================================================================
           GITHUB AI BRAIN - MERGE WARS EDITION           
================================================================

An intelligent AI companion for repository management
Powered by Model Context Protocol (MCP)
Bringing balance to the repository chaos!

Type 'help' for available commands
Type 'demo' to see example queries
Type 'exit' to quit
""")
        
        # Check GitHub token status
        if not os.getenv('GITHUB_TOKEN'):
            print("""
NOTICE: GitHub token not detected
   * You'll have limited API access (60 requests/hour)
   * Set GITHUB_TOKEN environment variable for full access
   * Get a token at: https://github.com/settings/tokens
""")
        else:
            print("GitHub token detected - Full API access enabled!")
    
    def show_help(self):
        """Display help information"""
        print("""
GITHUB AI BRAIN HELP

Natural Language Queries:
   * "Analyze microsoft/vscode repository"
   * "Show issues in facebook/react"
   * "List pull requests in kubernetes/kubernetes"
   * "Get recent commits from tensorflow/tensorflow"
   * "Check workflow status in pytorch/pytorch"
   * "Compare tensorflow/tensorflow vs pytorch/pytorch"

Special Commands:
   * help, h, ?     - Show this help
   * demo           - Show example queries
   * clear, cls     - Clear screen
   * exit, quit, q  - Exit the program

Features:
   * Repository health analysis
   * Multi-repository comparison
   * Issue and PR tracking
   * Workflow monitoring
   * Commit history analysis
   * Natural language processing

Repository Format:
   Always use 'owner/repository' format (e.g., 'microsoft/vscode')
""")
    
    def run_demo(self):
        """Run demonstration queries"""
        demo_queries = [
            "Analyze microsoft/vscode repository",
            "Show issues in facebook/react",
            "List pull requests in kubernetes/kubernetes",
            "Get recent commits from tensorflow/tensorflow",
            "Compare tensorflow/tensorflow vs pytorch/pytorch"
        ]
        
        print("""
DEMO MODE - Example Queries

Here are some example queries you can try:
""")
        
        for i, query in enumerate(demo_queries, 1):
            print(f"{i}. \"{query}\"")
        
        print("\nTry typing any of these queries, or create your own!")
        print("You can mix and match repositories and actions.")
        
        # Ask if user wants to run a demo query
        try:
            choice = input("\nWant to run a demo query? Enter 1-5 or press Enter to skip: ").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= 5:
                selected_query = demo_queries[int(choice) - 1]
                print(f"\nRunning demo query: \"{selected_query}\"")
                print("Processing...")
                
                response = self.agent.query(selected_query)
                print(f"\n{response}")
                
        except (ValueError, KeyboardInterrupt):
            print("\nDemo skipped. Ready for your queries!")
    
    def get_repositories_from_input(self) -> List[str]:
        """Get repository list from user input"""
        repos = []
        print("\nEnter repositories (owner/repo format, one per line):")
        print("Press Enter twice when done")
        
        while True:
            try:
                repo = input("Repository: ").strip()
                if not repo:
                    break
                if '/' in repo:
                    repos.append(repo)
                else:
                    print("Please use owner/repo format (e.g., microsoft/vscode)")
            except KeyboardInterrupt:
                break
        
        return repos

def main():
    """Main entry point for CLI"""
    try:
        cli = GitHubCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
