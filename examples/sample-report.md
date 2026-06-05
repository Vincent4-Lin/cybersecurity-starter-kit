# Repository Security Check

Path: /example/insecure-repo
Score: 63/100
Findings: 3

## 1. [HIGH] Sensitive-looking file found

- Check: `sensitive-file`
- Detail: `.env` looks like a secret or private key file.
- Recommendation: Remove the file from the repository and rotate any exposed credentials.

## 2. [MEDIUM] Security policy is missing

- Check: `missing-security-policy`
- Detail: No `SECURITY.md` file was found.
- Recommendation: Add `SECURITY.md` with supported versions and vulnerability reporting instructions.

## 3. [LOW] License is missing

- Check: `missing-license`
- Detail: No top-level license file was found.
- Recommendation: Add a license if this repository will be public.

