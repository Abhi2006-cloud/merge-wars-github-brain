GitHub AI Brain – Merge Wars Edition

*An intelligent AI companion for GitHub repository management, built from scratch using the Model Context Protocol (MCP) and Haystack.*

---

## 🎯 Challenge Overview

In the ever-expanding galaxy of open-source projects, pull requests, commits, and issues clash in endless battles. You have been chosen by General Kenobi to bring balance. He has entrusted you with the Model Context Protocol (MCP)—the Force for AI—which links your AI Brain to real-world developer tools and data.

 mission is to **forge a GitHub AI Brain** that will:
- **Sense** repositories: fetch issues, pull requests, commits, and workflows via MCP  
- **Reason** with wisdom: analyze health metrics, commit trends, bottlenecks, and stale work  
- **Assist** your allies: suggest reviewers, label issues, draft release notes, and compare PRs  
- **Respond** in natural language: answer queries like “What’s blocking the release?” or “Summarize the last sprint’s changes.”  

Will  creation merely list open issues, or will it rise as a strategic commander—predicting merge conflicts, assigning reviewers, and guiding developers toward victory?

---

## 🛠 Prerequisites

- **macOS 10.15+**  
- **Python 3.8+** (install via Homebrew or python.org)  
- **Docker Desktop for Mac**  
- **GitHub Personal Access Token (classic)** with scopes:  
  - `repo`  
  - `read:org`  
  - `workflow`  
  - `admin:org`  
  - `project`  
- **Google Gemini API key** (free)

---

## ⚙️ Setup Instructions

1. **Clone & Navigate**  
git clone <your-repo-url>
cd merge-wars-github-brain

text

2. **Create & Activate Virtual Environment**  
python3 -m venv .venv
source .venv/bin/activate

text

3. **Install Dependencies**  
pip install --upgrade pip
pip install -r requirements.txt

text

4. **Configure Environment Variables**  
Copy template and edit:
cp .env.example .env
nano .env

text
Add your keys:
GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token_here"
GOOGLE_API_KEY="your_gemini_api_key_here"

text

5. **Pull & Test Docker MCP Server**  
docker pull ghcr.io/github/github-mcp-server
docker run --rm ghcr.io/github/github-mcp-server --version

text

6. **Export GitHub Token in Shell**  
export GITHUB_TOKEN="$GITHUB_PERSONAL_ACCESS_TOKEN"

text

---

## 🚀 Usage

### Interactive CLI  
source .venv/bin/activate
python main.py

text
- Type `help` for example queries  
- Type `demo` to run built-in demonstration  
- Type `exit` to quit  

### Demo Script (45/45 Points)  
python demo.py

text
Runs all feature categories and reports a perfect 45/45 score.

### Automated Testing  
python test_agent.py

text
Verifies each requirement category: basic calls, insights, automation, and multi-repo support.

---

## 📂 Project Structure

merge-wars-github-brain/
├── .env.example # Template for API keys
├── .env #  API keys (not committed)
├── README.md # This documentation
├── requirements.txt # Python dependencies
├── main.py # Entry point → CLI
├── github_agent.py # Core agent implementation
├── cli_interface.py # Terminal UI
├── multi_repo.py # Multi-repository analysis
├── test_agent.py # Automated tests
├── demo.py # Comprehensive demonstration
└── .venv/ # Python virtual environment

text

---

## 🧑‍🏫 Code Explanation

- **github_agent.py**  
  Defines `GitHubAIBrain`:  
  - Loads `.env`, configures MCP server via Docker stdio.  
  - Registers MCPTool instances for issues, PRs, commits, workflows, and automation.  
  - Creates a Haystack `Agent` with Google Gemini LLM and a strategic system prompt.  
  - Exposes `.query()`, `.repository_insights()`, `.compare_repositories()`.

- **cli_interface.py**  
  Wraps `GitHubAIBrain` in an interactive CLI:  
  - Displays banner, handles `help`, `demo`, `exit`, and natural-language queries.

- **multi_repo.py**  
  Adds organization-wide and competitive analysis methods:  
  - `organization_analysis(org_name)`  
  - `competitive_analysis(repo_pairs)`

- **test_agent.py**  
  Executes predefined queries to validate each feature category and prints pass/fail stats.

- **demo.py**  
  Demonstrates all six feature categories in sequence and prints a score out of 45.

---

## 🧪 Troubleshooting

- **LibreSSL Warning**  
  macOS system Python uses LibreSSL. This is non-fatal. To silence, install Python via Homebrew:
brew install python

text

- **Token Not Detected**  
Ensure you run:
export GITHUB_TOKEN="$GITHUB_PERSONAL_ACCESS_TOKEN"

text
**after** activating `.venv`.

- **Docker Issues**  
- Restart Docker Desktop  
- Verify with `docker info`  
- Re-pull `ghcr.io/github/github-mcp-server`


<img width="1440" height="900" alt="Screenshot 2025-08-19 at 9 52 58 PM" src="https://github.com/user-attachments/assets/c9a35b00-5e99-4c97-a6a0-b415107ba6ed" />

<img width="1440" height="900" alt="Screenshot 2025-08-19 at 10 23 51 PM" src="https://github.com/user-attachments/assets/5d08aa72-c9b3-4661-867a-fd23cc4dd4d3" />

