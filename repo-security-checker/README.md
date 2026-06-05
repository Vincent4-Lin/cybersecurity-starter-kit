# Repo Security Checker

`check_repo_security.py` is a small Python CLI that checks a local repository or GitHub URL for basic security hygiene.

It is intentionally simple and dependency-free. It is not a replacement for tools such as Gitleaks, Trivy, CodeQL, or professional security review.

## Usage

```bash
python3 repo-security-checker/check_repo_security.py /path/to/repo
```

Scan a public GitHub repository:

```bash
python3 repo-security-checker/check_repo_security.py https://github.com/owner/repo
```

The tool clones GitHub URLs with `git clone --depth 1` into a temporary folder, scans the cloned files, and removes the temporary clone when it finishes.

Output JSON:

```bash
python3 repo-security-checker/check_repo_security.py https://github.com/owner/repo --format json
```

Fail CI on high severity findings:

```bash
python3 repo-security-checker/check_repo_security.py . --fail-on high
```

## Checks

- Missing `README.md`.
- Missing `LICENSE`.
- Missing `SECURITY.md`.
- Missing `.gitignore`.
- Sensitive-looking files such as `.env`, private keys, and certificate key files.
- Common hardcoded secret patterns.
- Dependency files without Dependabot configuration.
- Dependency files without GitHub Actions workflows.
- GitHub Actions workflows without explicit permissions.
- `pull_request_target` workflow usage.

## Example

```text
# Repository Security Check

Scanned path: /example/repo
Score: 82/100
Findings: 2

## 1. [MEDIUM] Security policy is missing

- Check: `missing-security-policy`
- Detail: No SECURITY.md file was found.
- Recommendation: Add SECURITY.md with supported versions and vulnerability reporting instructions.
```
