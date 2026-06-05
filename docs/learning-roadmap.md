# Cybersecurity Learning Roadmap

This roadmap is meant for a beginner who wants a clear path without getting lost in random tool lists.

## 1. Foundations

Learn enough system and network basics to understand what security tools are reporting.

- Linux command line: files, permissions, processes, services, logs.
- Networking: IP, DNS, HTTP, TLS, ports, routing, firewalls.
- Git and GitHub: commits, branches, pull requests, Actions, secrets.
- Basic Python or JavaScript: enough to read scripts and automate checks.

Suggested practice:

- Use Linux in a VM or container.
- Read HTTP requests and responses in browser devtools.
- Create small scripts that parse files or call APIs.

## 2. Web Application Security

Focus on the OWASP Top 10 categories first.

- Broken access control.
- Cryptographic failures.
- Injection.
- Insecure design.
- Security misconfiguration.
- Vulnerable and outdated components.
- Identification and authentication failures.
- Software and data integrity failures.
- Security logging and monitoring failures.
- Server-side request forgery.

Suggested practice:

- PortSwigger Web Security Academy.
- OWASP Juice Shop.
- Write short notes for each lab: what happened, why it mattered, and how to fix it.

## 3. Defensive Tooling

Learn tools that help teams prevent or detect issues.

- Secret scanning: Gitleaks, TruffleHog.
- Vulnerability scanning: Trivy, OSV-Scanner, Nuclei.
- Repository hygiene: Dependabot, CodeQL, security policy files.
- Detection engineering: Sigma, MITRE ATT&CK.
- Monitoring and response: Wazuh, Security Onion, Zeek, Suricata.

## 4. Cloud And Supply Chain Security

Modern systems depend on packages, containers, infrastructure, and CI/CD.

- Scan dependencies and container images.
- Review GitHub Actions workflows.
- Avoid long-lived secrets in code and CI logs.
- Learn SBOM basics.
- Understand least privilege for cloud IAM.

## 5. Build Public Proof Of Learning

Good GitHub projects do not need to be huge. They need to be clear and useful.

- Publish notes with sources and defensive takeaways.
- Add checklists that someone else can reuse.
- Build small tools that solve a narrow problem.
- Keep examples safe and focused on authorized environments.

