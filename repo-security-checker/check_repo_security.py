#!/usr/bin/env python3
"""Check basic security hygiene for a local repository or GitHub URL."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "target",
    "vendor",
}

TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".conf",
    ".env",
    ".ini",
    ".json",
    ".lock",
    ".md",
    ".py",
    ".ps1",
    ".psd1",
    ".psm1",
    ".rb",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
    ".js",
    ".jsx",
}

SECRET_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_ed25519",
}

SECRET_FILE_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}

SECRET_PATTERNS = [
    (
        "aws-access-key",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "Possible AWS access key found.",
    ),
    (
        "private-key",
        re.compile(r"-----BEGIN (RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"),
        "Possible private key block found.",
    ),
    (
        "assigned-secret",
        re.compile(
            r"(?i)\b(api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|secret)\b"
            r"\s*[:=]\s*['\"]?[A-Za-z0-9_\-./+=]{16,}"
        ),
        "Possible hardcoded secret assignment found.",
    ),
]

SEVERITY_WEIGHT = {
    "high": 25,
    "medium": 12,
    "low": 6,
    "info": 0,
}


@dataclass(frozen=True)
class Finding:
    severity: str
    check_id: str
    title: str
    detail: str
    recommendation: str


@dataclass(frozen=True)
class Report:
    path: str
    score: int
    findings: list[Finding]
    source: str | None = None


def has_any_file(root: Path, candidates: Iterable[str]) -> bool:
    return any((root / candidate).is_file() for candidate in candidates)


def has_any_glob(root: Path, patterns: Iterable[str]) -> bool:
    for pattern in patterns:
        if any(root.glob(pattern)):
            return True
    return False


def iter_repo_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def is_probably_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


def read_text_safely(path: Path, max_bytes: int = 1_000_000) -> str | None:
    try:
        if path.stat().st_size > max_bytes:
            return None
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def normalize_github_url(value: str) -> str | None:
    """Return a cloneable GitHub URL when the input looks like one."""
    value = value.strip()

    ssh_match = re.fullmatch(r"git@github\.com:([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?", value)
    if ssh_match:
        owner, repo = ssh_match.groups()
        return f"git@github.com:{owner}/{repo}.git"

    parsed = urlparse(value if "://" in value else f"https://{value}")
    if parsed.netloc.lower() != "github.com":
        return None

    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None

    owner = parts[0]
    repo = parts[1].removesuffix(".git")
    valid_name = re.compile(r"^[A-Za-z0-9_.-]+$")
    if not valid_name.fullmatch(owner) or not valid_name.fullmatch(repo):
        return None

    return f"https://github.com/{owner}/{repo}.git"


def check_basic_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    if not has_any_file(root, ["README.md", "README.txt", "README"]):
        findings.append(
            Finding(
                "medium",
                "missing-readme",
                "README is missing",
                "The repository does not have a top-level README file.",
                "Add a README that explains purpose, setup, usage, and safety assumptions.",
            )
        )

    if not has_any_file(root, ["LICENSE", "LICENSE.md", "COPYING"]):
        findings.append(
            Finding(
                "low",
                "missing-license",
                "License is missing",
                "No top-level license file was found.",
                "Add a license if this repository will be public.",
            )
        )

    if not has_any_file(root, ["SECURITY.md", ".github/SECURITY.md"]):
        findings.append(
            Finding(
                "medium",
                "missing-security-policy",
                "Security policy is missing",
                "No SECURITY.md file was found.",
                "Add SECURITY.md with supported versions and vulnerability reporting instructions.",
            )
        )

    if not has_any_file(root, [".gitignore"]):
        findings.append(
            Finding(
                "medium",
                "missing-gitignore",
                ".gitignore is missing",
                "No top-level .gitignore file was found.",
                "Add .gitignore entries for secrets, local files, build output, and dependencies.",
            )
        )

    return findings


def check_secret_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    for path in iter_repo_files(root):
        name = path.name
        suffix = path.suffix.lower()
        if name in SECRET_FILE_NAMES or suffix in SECRET_FILE_SUFFIXES:
            findings.append(
                Finding(
                    "high",
                    "sensitive-file",
                    "Sensitive-looking file found",
                    f"{path.relative_to(root)} looks like a secret or private key file.",
                    "Remove the file from the repository and rotate any exposed credentials.",
                )
            )

    return findings


def check_secret_patterns(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    for path in iter_repo_files(root):
        if not is_probably_text(path):
            continue

        content = read_text_safely(path)
        if content is None:
            continue

        for check_id, pattern, message in SECRET_PATTERNS:
            match = pattern.search(content)
            if not match:
                continue
            line_number = content[: match.start()].count("\n") + 1
            findings.append(
                Finding(
                    "high",
                    check_id,
                    "Possible secret in source",
                    f"{message} Location: {path.relative_to(root)}:{line_number}.",
                    "Remove the secret, rotate it, and store future secrets in a secure secret manager.",
                )
            )
            break

    return findings


def check_dependency_security(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    dependency_files = [
        "package.json",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "requirements.txt",
        "Pipfile",
        "poetry.lock",
        "pyproject.toml",
        "go.mod",
        "Cargo.toml",
        "Gemfile",
        "pom.xml",
        "build.gradle",
    ]

    has_dependencies = has_any_file(root, dependency_files)
    has_dependabot = has_any_file(root, [".github/dependabot.yml", ".github/dependabot.yaml"])
    has_workflows = has_any_glob(root, [".github/workflows/*.yml", ".github/workflows/*.yaml"])

    if has_dependencies and not has_dependabot:
        findings.append(
            Finding(
                "medium",
                "missing-dependabot",
                "Dependency update automation is missing",
                "Dependency files were found, but no Dependabot configuration was detected.",
                "Add .github/dependabot.yml or document another dependency update process.",
            )
        )

    if has_dependencies and not has_workflows:
        findings.append(
            Finding(
                "low",
                "missing-ci-security-scan",
                "No GitHub Actions workflow detected",
                "Dependency files were found, but no GitHub Actions workflow was detected.",
                "Add CI checks for tests and security scanning such as Trivy, OSV-Scanner, or CodeQL.",
            )
        )

    return findings


def check_github_actions(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    workflow_files = list(root.glob(".github/workflows/*.yml")) + list(root.glob(".github/workflows/*.yaml"))
    for workflow in workflow_files:
        content = read_text_safely(workflow)
        if content is None:
            continue

        relative = workflow.relative_to(root)
        if "permissions:" not in content:
            findings.append(
                Finding(
                    "medium",
                    "workflow-missing-permissions",
                    "Workflow permissions are not explicit",
                    f"{relative} does not define a permissions block.",
                    "Set explicit least-privilege GitHub Actions permissions.",
                )
            )

        if re.search(r"(?i)pull_request_target", content):
            findings.append(
                Finding(
                    "medium",
                    "workflow-uses-pull-request-target",
                    "Workflow uses pull_request_target",
                    f"{relative} uses pull_request_target, which can expose privileged context if misused.",
                    "Review whether pull_request is sufficient and avoid checking out untrusted code with secrets.",
                )
            )

    return findings


def calculate_score(findings: list[Finding]) -> int:
    penalty = sum(SEVERITY_WEIGHT[finding.severity] for finding in findings)
    return max(0, 100 - penalty)


def run_checks(root: Path, source: str | None = None) -> Report:
    root = root.resolve()
    findings: list[Finding] = []
    findings.extend(check_basic_files(root))
    findings.extend(check_secret_files(root))
    findings.extend(check_secret_patterns(root))
    findings.extend(check_dependency_security(root))
    findings.extend(check_github_actions(root))
    return Report(path=str(root), score=calculate_score(findings), findings=findings, source=source)


def clone_repository(url: str, destination_root: Path) -> Path:
    destination = destination_root / "repo"
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", url, str(destination)],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("git is not installed or not available in PATH.") from exc
    except subprocess.CalledProcessError as exc:
        error = exc.stderr.strip() or exc.stdout.strip() or "unknown git clone error"
        raise RuntimeError(f"failed to clone repository: {error}") from exc
    return destination


def scan_target(target: str) -> Report:
    github_url = normalize_github_url(target)
    if github_url is not None:
        with tempfile.TemporaryDirectory(prefix="repo-security-checker-") as directory:
            clone_path = clone_repository(github_url, Path(directory))
            return run_checks(clone_path, source=github_url)

    root = Path(target)
    if not root.exists() or not root.is_dir():
        raise ValueError(f"{target} is not a directory or supported GitHub URL")

    return run_checks(root)


def render_text(report: Report) -> str:
    lines = [
        "# Repository Security Check",
        "",
    ]
    if report.source:
        lines.append(f"Source: {report.source}")
    lines.extend(
        [
            f"Scanned path: {report.path}",
            f"Score: {report.score}/100",
            f"Findings: {len(report.findings)}",
            "",
        ]
    )

    if not report.findings:
        lines.append("No findings. Basic repository hygiene looks good.")
        return "\n".join(lines)

    grouped = sorted(report.findings, key=lambda item: SEVERITY_WEIGHT[item.severity], reverse=True)
    for index, finding in enumerate(grouped, start=1):
        lines.extend(
            [
                f"## {index}. [{finding.severity.upper()}] {finding.title}",
                "",
                f"- Check: `{finding.check_id}`",
                f"- Detail: {finding.detail}",
                f"- Recommendation: {finding.recommendation}",
                "",
            ]
        )

    return "\n".join(lines).rstrip()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check basic security hygiene for a local repository or GitHub URL.")
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Repository path or GitHub URL to scan. Defaults to current directory.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format. Defaults to text.",
    )
    parser.add_argument(
        "--fail-on",
        choices=["none", "high", "medium", "low"],
        default="none",
        help="Exit with code 1 if findings at this severity or higher are present.",
    )
    return parser.parse_args(argv)


def should_fail(findings: list[Finding], threshold: str) -> bool:
    if threshold == "none":
        return False
    severity_order = {"low": 1, "medium": 2, "high": 3}
    minimum = severity_order[threshold]
    return any(severity_order.get(finding.severity, 0) >= minimum for finding in findings)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    try:
        report = scan_target(args.target)
    except (RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(asdict(report), indent=2))
    else:
        print(render_text(report))

    return 1 if should_fail(report.findings, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
