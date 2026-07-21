#!/usr/bin/env sh
# Mount the canonical protocol store into each detected runtime skill folder.
# Default store: $PROTO_STORE or ~/.protocols. Uses symlinks.
#
# Usage:
#   sh scripts/sync_store.sh            # link both runtimes
#   sh scripts/sync_store.sh --pull     # git pull the store first
#   sh scripts/sync_store.sh --push     # git commit + push the store after
set -e
STORE="${PROTO_STORE:-$HOME/.protocols}"
PROTO_DIR="$STORE/protocols"
INBOX_DIR="$STORE/inbox"
mkdir -p "$PROTO_DIR" "$INBOX_DIR"

[ "$1" = "--pull" ] && [ -d "$STORE/.git" ] && git -C "$STORE" pull --ff-only

link_runtime() {
  name="$1"; skill="$2"
  [ -d "$skill" ] || { echo "skip $name: not installed at $skill"; return; }
  ref="$skill/references"
  mkdir -p "$ref"
  ln -sfn "$PROTO_DIR" "$ref/protocols"
  echo "linked $name: $ref/protocols -> $PROTO_DIR"
}

link_runtime "claude-code" "$HOME/.claude/skills/proto"
link_runtime "codex" "$HOME/.codex/skills/proto"

[ "$1" = "--push" ] && [ -d "$STORE/.git" ] && {
  git -C "$STORE" add -A
  git -C "$STORE" commit -m "sync protocols" 2>/dev/null || true
  git -C "$STORE" push
}
