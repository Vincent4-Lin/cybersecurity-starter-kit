# Cybersecurity Starter Kit

A practical starter kit for learning cybersecurity and checking the basic security hygiene of a GitHub-style repository.

This project has two parts:

1. A curated learning kit for cybersecurity fundamentals, tools, labs, and checklists.
2. A small command-line tool that checks whether a repository has basic security files and risky patterns.

The goal is to stay beginner-friendly while still producing something useful enough to share on GitHub.

For a Traditional Chinese explanation of what this project does, see [PROJECT_OVERVIEW.zh-TW.md](PROJECT_OVERVIEW.zh-TW.md).

## Portfolio Position

This repository is the learning and repository-hygiene layer of my portfolio. It is not a main research prototype like [ai-soc-analyst](https://github.com/Vincent4-Lin/ai-soc-analyst). Instead, it shows my study roadmap, basic security checklists, and a practical Python checker for GitHub-style repository hygiene.

It supports the larger portfolio by documenting the foundations behind my defensive security projects.

## What's Inside

```text
.
├── checklists/
│   ├── github-repo-security.md
│   └── web-app-security.md
├── docs/
│   ├── labs.md
│   ├── learning-roadmap.md
│   ├── pre-push-security-checks.md
│   └── tools.md
├── examples/
│   └── sample-report.md
├── notes/
│   └── README.md
├── repo-security-checker/
│   ├── README.md
│   └── check_repo_security.py
└── tests/
    └── test_check_repo_security.py
```

## Quick Start

Run the repository checker against any local project:

```bash
python3 repo-security-checker/check_repo_security.py /path/to/repo
```

Run it against this starter kit:

```bash
python3 repo-security-checker/check_repo_security.py .
```

Install the pre-push hook so Git runs the checker automatically before `git push`:

```bash
sh scripts/install-pre-push-hook.sh
```

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install-pre-push-hook.ps1
```

Run it against a public GitHub repository URL:

```bash
python3 repo-security-checker/check_repo_security.py https://github.com/owner/repo
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

## Learning Path

Start with [docs/learning-roadmap.md](docs/learning-roadmap.md), then use:

- [docs/tools.md](docs/tools.md) to learn common defensive and AppSec tools.
- [docs/labs.md](docs/labs.md) to find safe practice environments.
- [docs/pre-push-security-checks.md](docs/pre-push-security-checks.md) to understand what you can check before pushing to GitHub.
- [checklists/github-repo-security.md](checklists/github-repo-security.md) to review repository hygiene.
- [checklists/web-app-security.md](checklists/web-app-security.md) to review common web app risks.

## Project Ideas To Extend

- Add scoring by severity.
- Add checks for Dependabot, CodeQL, or secret scanning configuration.
- Add a `docs/writeups/` folder for PortSwigger Academy or OWASP Juice Shop notes.
- Build a small web UI that displays the checker result.

## Safety Note

This repository is focused on learning, defensive security, and authorized testing. Only test systems you own or have explicit permission to assess.
