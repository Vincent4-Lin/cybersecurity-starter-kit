$ErrorActionPreference = "Stop"

$root = (& git rev-parse --show-toplevel 2>$null).Trim()
if (-not $root) {
    Write-Error "This script must be run inside a Git repository."
    exit 1
}

$checker = Join-Path $root "repo-security-checker/check_repo_security.py"
if (-not (Test-Path $checker)) {
    Write-Error "Cannot find repo-security-checker/check_repo_security.py from repository root."
    exit 1
}

$hookDir = Join-Path $root ".git/hooks"
$hookFile = Join-Path $hookDir "pre-push"

New-Item -ItemType Directory -Force -Path $hookDir | Out-Null

$hookContent = @'
#!/bin/sh
set -eu

ROOT="$(git rev-parse --show-toplevel)"
CHECKER="$ROOT/repo-security-checker/check_repo_security.py"

echo "Running repository security check before push..."

python3 "$CHECKER" "$ROOT" --fail-on high

echo "Repository security check passed."
'@

[System.IO.File]::WriteAllText($hookFile, $hookContent + "`n", [System.Text.Encoding]::ASCII)

$chmod = Get-Command chmod -ErrorAction SilentlyContinue
if ($chmod) {
    & chmod +x $hookFile
}

Write-Host "Installed pre-push hook:"
Write-Host $hookFile

