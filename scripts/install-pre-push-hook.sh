#!/bin/sh
set -eu

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
HOOK_DIR="$ROOT/.git/hooks"
HOOK_FILE="$HOOK_DIR/pre-push"
CHECKER="repo-security-checker/check_repo_security.py"

if [ ! -f "$ROOT/$CHECKER" ]; then
  echo "error: cannot find $CHECKER from repository root" >&2
  exit 1
fi

mkdir -p "$HOOK_DIR"

cat > "$HOOK_FILE" <<'HOOK'
#!/bin/sh
set -eu

ROOT="$(git rev-parse --show-toplevel)"
CHECKER="$ROOT/repo-security-checker/check_repo_security.py"

echo "Running repository security check before push..."

python3 "$CHECKER" "$ROOT" --fail-on high

echo "Repository security check passed."
HOOK

chmod +x "$HOOK_FILE"

echo "Installed pre-push hook:"
echo "$HOOK_FILE"

