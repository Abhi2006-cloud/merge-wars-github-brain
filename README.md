# GitHub AI Brain — Merge Wars Edition

An intelligent repository analysis and benchmarking engine that evaluates project health, contributor velocity, issue dynamics, and CI/CD workflow statuses across individual repositories and entire organizations.

---

## Why This Project?

Managing multiple open-source or enterprise software repositories requires continuous visibility into contributor velocity, open issue bottlenecks, pull request review latency, and CI/CD build stability. Manually tracking these metrics across dozens of repositories is inefficient and fragmented.

**GitHub AI Brain** addresses this engineering challenge by aggregating raw metadata from the GitHub API into actionable metrics. It calculates an objective **Activity Health Score (0–100)** based on contribution recency and issue/PR resolution patterns, providing developers, engineering managers, and open-source maintainers with immediate insights through natural language terminal queries.

---

## Features

- 🏥 **Repository Health Scoring**: Computes a weighted 0–100 activity score and assigns health ratings (`🟢 Excellent`, `🟡 Good`, `🟠 Fair`, `🔴 Needs Attention`) based on recent commits, issues, and PR velocity.
- 📊 **Competitive Benchmarking**: Performs side-by-side comparative analysis between competing or related repositories (e.g. `tensorflow/tensorflow` vs `pytorch/pytorch`).
- 🏢 **Organization-Level Audits**: Aggregates total stars, forks, open issue bottlenecks, and average activity scores across an entire GitHub organization (e.g. `facebook`, `microsoft`).
- ⚙️ **CI/CD Workflow Monitoring**: Tracks GitHub Actions run conclusions and highlights failing build pipelines.
- 💬 **Natural Language Query Interface**: Routes user queries to specific sub-systems using pattern-matching and intent detection.
- 🔑 **Resilient Rate-Limit Handling**: Supports authenticated execution (5,000 req/hr) with graceful degradation under unauthenticated mode (60 req/hr).

---

## Architecture

```text
┌─────────────────────────────────────────────────────────┐
│                 Terminal Interface Layer                │
│            (main.py / cli_interface.py / demo.py)       │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│              Natural Language Query Router              │
│               (Intent & Handle Extraction)              │
└──────────────┬───────────────────────────┬──────────────┘
               │                           │
               ▼                           ▼
┌─────────────────────────────┐ ┌─────────────────────────┐
│    GitHubAIBrain Agent      │ │    MultiRepoAnalyzer    │
│  (Health Scoring Engine)    │ │   (Org Audit Engine)    │
└──────────────┬──────────────┘ └──────────┬──────────────┘
               │                           │
               └─────────────┬─────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                 GitHub REST API Service                 │
│               (httprequests / endpoints)                │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
                 GitHub Cloud Infrastructure
```

---

## Tech Stack

- **Core Runtime**: Python 3.8+
- **API Integration**: GitHub REST API v3 via `requests`
- **Environment Management**: `python-dotenv`
- **Testing & Verification**: `pytest` unit test suite with mocked API dependencies & `unittest` integration tests
- **Architecture Pattern**: Modular OOP with decoupled interface, core agent, and multi-repo analysis layers

---

## Project Structure

```text
merge-wars-github-brain/
├── main.py              # CLI entry point script
├── github_agent.py      # Core GitHubAIBrain engine & health scoring logic
├── multi_repo.py        # Organization-level auditor & multi-repo benchmarking
├── cli_interface.py     # Interactive terminal user interface & banner rendering
├── demo.py              # Comprehensive feature demonstration script
├── test_agent.py        # Integration test suite
├── tests/               # Unit test suite with offline mocks
│   ├── test_github_agent.py
│   └── test_multi_repo.py
├── requirements.txt     # Python runtime & testing dependencies
├── .env.example         # Template environment variable configuration
└── .gitignore            # Git exclusion rules
```

---

## Getting Started

### Prerequisites

- **Python**: 3.8 or higher
- **GitHub Personal Access Token** *(Optional, recommended)*: Classic token with `repo` and `read:org` scopes for 5,000 requests/hour limit.

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/merge-wars-github-brain.git
   cd merge-wars-github-brain
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your GitHub token:
   ```env
   GITHUB_TOKEN=ghp_your_actual_token_here
   ```

5. **Run Unit Tests**
   ```bash
   python3 -m pytest tests/
   ```

6. **Start Interactive Application**
   ```bash
   python3 main.py
   ```

---

## Environment Variables

| Variable Name | Required | Default | Description |
| :--- | :---: | :---: | :--- |
| `GITHUB_TOKEN` | Optional | `None` | Personal Access Token for GitHub API access (increases rate limit from 60 to 5,000 req/hr). |

---

## Usage & Commands

### Natural Language Query Examples

Launch `python3 main.py` and run any of the following queries:

- **Repository Health Audit**:
  ```text
  [GitHub AI Brain] > Analyze microsoft/vscode repository
  ```
- **Competitive Benchmarking**:
  ```text
  [GitHub AI Brain] > Compare tensorflow/tensorflow vs pytorch/pytorch
  ```
- **Organization Audit**:
  ```text
  [GitHub AI Brain] > Analyze organization facebook
  ```
- **Issue Audit**:
  ```text
  [GitHub AI Brain] > Show open issues in facebook/react
  ```
- **Pull Request Velocity**:
  ```text
  [GitHub AI Brain] > List pull requests in kubernetes/kubernetes
  ```
- **Workflow Run Monitoring**:
  ```text
  [GitHub AI Brain] > Check workflow status in pytorch/pytorch
  ```

### Special Built-In Commands

- `help` / `h` / `?`: Display detailed usage instructions.
- `demo`: Run interactive demo selection menu.
- `clear` / `cls`: Clear terminal output.
- `exit` / `quit` / `q`: Exit application safely.

### Automated Demo & Integration Tests

```bash
# Run comprehensive demo script
python3 demo.py

# Run integration tests against live GitHub API
python3 test_agent.py
```

---

## Engineering Decisions

1. **GitHub REST API v3 over GraphQL**: Selected REST API v3 for high reliability and zero schema overhead when accessing public metadata across diverse user repositories without mandatory OAuth scope escalation.
2. **Weighted Activity Score Model**: The 0–100 health score balances recent commit frequency (40 points max), issue updates (30 points max), and pull request resolution velocity (30 points max), evaluating project activity over a 30-day sliding window.
3. **Decoupled System Layers**: Seperate modules for API interaction (`github_agent.py`), multi-repository/organization aggregation (`multi_repo.py`), and presentation (`cli_interface.py`) ensure maintainability and testability.
4. **Mocked Unit Test Strategy**: Used `pytest` with mocked response fixtures to achieve fast (<2s), offline test execution without consuming GitHub API quotas.

---

## Security

- **Environment Isolation**: Secrets are loaded exclusively via environment variables (`python-dotenv`); `.env` is explicitly ignored by `.gitignore`.
- **Zero Token Persistence**: Authentication tokens are passed via HTTP headers in-memory and are never cached or logged to disk.
- **Input Sanitization**: Regex extraction cleans user strings to prevent injection or invalid URI generation.

---

## Testing

```bash
# Execute fast, offline unit test suite
python3 -m pytest tests/ -v
```

The test suite covers:
- Weighted activity score calculations
- ISO timestamp recency evaluation (`_is_recent`)
- Workflow run status aggregation
- Intent & repository handle regex extraction
- Organization report markdown formatting
- API response exception handling

---

## Deployment

The application is designed to run in any Python 3.8+ environment or Docker container:

```bash
# Run via Docker (if containerized)
docker build -t github-ai-brain .
docker run --rm -e GITHUB_TOKEN=$GITHUB_TOKEN github-ai-brain
```

---

## Future Improvements

- **GraphQL API Integration**: Add optional GraphQL endpoint support for bulk metadata queries.
- **Local Response Caching**: Introduce SQLite or Redis caching to store repository metadata and respect rate limits.
- **Export Capabilities**: Add JSON/CSV export options for organization audit reports.
