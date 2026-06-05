# GitHub Repository Security Checklist

Use this checklist when reviewing a repository before publishing or contributing.

## Basic Files

- [ ] `README.md` explains the project purpose and usage.
- [ ] `LICENSE` exists if the project is public.
- [ ] `.gitignore` excludes local secrets, build outputs, virtual environments, and dependency folders.
- [ ] `SECURITY.md` explains how to report security issues.
- [ ] Dependencies are documented.

## Secrets

- [ ] No `.env` file is committed.
- [ ] No private keys are committed.
- [ ] No API keys or tokens appear in source files.
- [ ] GitHub Actions logs do not print secrets.
- [ ] CI uses GitHub secrets or a secure secret manager.

## Dependency Security

- [ ] Dependabot or another update workflow is configured.
- [ ] Lockfiles are committed when appropriate.
- [ ] Dependency scanner is used in CI.
- [ ] Vulnerable dependencies are triaged regularly.

## GitHub Actions

- [ ] Workflows use the minimum permissions needed.
- [ ] Third-party actions are pinned to trusted versions.
- [ ] Pull request workflows do not expose secrets to untrusted code.
- [ ] Build artifacts do not contain secrets.

## Documentation

- [ ] Security assumptions are documented.
- [ ] Threat model or risk notes exist for security-sensitive projects.
- [ ] Examples avoid real credentials and real production targets.

