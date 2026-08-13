# Contributing to GitHub AI Brain — Merge Wars Edition

Thank you for your interest in contributing to **GitHub AI Brain**! We welcome bug reports, feature suggestions, documentation updates, and code contributions.

---

## Code of Conduct

All contributors are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating.

---

## How to Contribute

### 1. Reporting Bugs

Before submitting a bug report, please check existing issues to avoid duplicates. When opening an issue, include:
- A clear, descriptive title.
- Steps to reproduce the issue.
- Expected behavior vs. actual behavior.
- Python version, operating system, and relevant error tracebacks.

### 2. Suggesting Enhancements

Feature requests are tracked via GitHub issues. Please explain:
- The problem your enhancement addresses.
- Your proposed solution or user experience.
- Any alternative approaches considered.

### 3. Submitting Pull Requests

1. **Fork the Repository**: Create a fork under your GitHub account.
2. **Clone & Setup**:
   ```bash
   git clone https://github.com/your-username/merge-wars-github-brain.git
   cd merge-wars-github-brain
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```
3. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/amazing-new-feature
   ```
4. **Make Your Changes**:
   - Ensure all code conforms to PEP 8 style standards.
   - Include docstrings and type annotations for all new functions/classes.
   - Add offline unit tests in `tests/` for new functionality.

5. **Run the Test Suite**:
   ```bash
   python3 -m pytest tests/ -v
   ```

6. **Commit & Push**:
   ```bash
   git commit -m "feat: add amazing new feature"
   git push origin feature/amazing-new-feature
   ```

7. **Open a Pull Request**: Submit your PR targeting the `main` branch with a clear title and description.

---

## Coding Standards & Style Guide

- **Style Guide**: Standard PEP 8 formatting.
- **Docstrings**: Google or NumPy style docstrings for classes and public methods.
- **Type Annotations**: Use Python standard type hints (`typing.Dict`, `typing.List`, `typing.Optional`, etc.).
- **Testing**: Maintain fast, offline unit tests using `unittest.mock` to avoid external API calls during testing.

Thank you for helping build a better repository intelligence engine! 🚀
