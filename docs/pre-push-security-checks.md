# Pre-Push Security Checks

GitHub has useful security features, but you should still check your project before pushing.

## What GitHub Can Check

GitHub can help after a repository exists on GitHub or during the push/upload process.

| GitHub feature | What it does | Why local checks still help |
|---|---|---|
| Secret scanning push protection | Blocks some supported secrets during push or file upload. | It does not catch every possible secret format, and you should catch problems before the push attempt. |
| Dependabot alerts | Warns about known vulnerable dependencies when the dependency graph changes or new advisories appear. | The repository and dependency files usually need to exist on GitHub first. |
| Code scanning / CodeQL | Finds security bugs in source code after code scanning is configured. | It must be configured, and it is heavier than a quick local hygiene check. |
| GitHub Actions | Runs automated checks after a workflow exists. | The workflow file itself can have risky permissions or unsafe triggers. |

## What You Can Check Before Pushing

Run a local check before you upload code:

```bash
python3 repo-security-checker/check_repo_security.py .
```

Or install the Git pre-push hook:

```bash
sh scripts/install-pre-push-hook.sh
```

After that, Git runs the checker automatically before every `git push` from this local clone.

This project checks:

- Whether basic public repo files exist: `README.md`, `LICENSE`, `SECURITY.md`, `.gitignore`.
- Whether sensitive-looking files exist: `.env`, private keys, certificate key files.
- Whether source files contain obvious hardcoded secret patterns.
- Whether dependency files exist without Dependabot.
- Whether dependency files exist without a GitHub Actions workflow.
- Whether GitHub Actions workflows define explicit permissions.
- Whether workflows use `pull_request_target`, which needs careful review.

## What This Tool Does Not Replace

Use this checker as a first pass, not as the only security tool.

For stronger checks, add:

- Gitleaks or TruffleHog for deeper secret scanning.
- Trivy or OSV-Scanner for dependency and container scanning.
- CodeQL for code scanning.
- Manual review for authentication, authorization, and business logic bugs.

## Simple Mental Model

```text
Before push:
  Run this local checker.
  Remove obvious risky files and missing security basics.

Optional automation:
  Install the pre-push hook.
  Git runs the checker automatically before push.

During push:
  GitHub push protection may block supported secrets.

After push:
  Dependabot, CodeQL, and GitHub Actions can keep checking over time.
```
