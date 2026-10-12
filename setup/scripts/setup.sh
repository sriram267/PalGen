#!/usr/bin/env bash
# Universal Multimodal Analysis Suite — macOS / Linux Setup
# Usage:
#   bash setup/scripts/setup.sh                  Install deps + create symlinks
#   bash setup/scripts/setup.sh --symlinks-only  Only recreate IDE symlinks
set -e

echo "==================================================================="
echo "    Universal Multimodal Analysis Suite — macOS / Linux Setup"
echo "==================================================================="
echo ""

OS="$(uname -s)"
echo "Detected OS: $OS"
echo ""

# Resolve workspace root (two levels up from setup/scripts/)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
echo "Workspace root: $ROOT_DIR"
echo ""

# ─── Symlink setup ─────────────────────────────────────────────────────────
setup_symlinks() {
    echo "--- Creating .agents/rules/ symlinks → setup/rules/ ---"
    mkdir -p "$ROOT_DIR/.agents/rules"

    for file in AGENTS.md GEMINI.md CLAUDE.md; do
        src="$ROOT_DIR/setup/rules/$file"
        dst_rules="$ROOT_DIR/.agents/rules/$file"
        if [ -f "$src" ]; then
            rm -f "$dst_rules"
            ln -s "../../setup/rules/$file" "$dst_rules"
            echo "  ✅ .agents/rules/$file → setup/rules/$file"
        fi
    done

    echo "--- Creating .cursor/rules/ symlinks → setup/rules/ ---"
    mkdir -p "$ROOT_DIR/.cursor/rules"
    if [ -f "$ROOT_DIR/setup/rules/agent-instructions.mdc" ]; then
        rm -f "$ROOT_DIR/.cursor/rules/agent-instructions.mdc"
        ln -s "../../setup/rules/agent-instructions.mdc" "$ROOT_DIR/.cursor/rules/agent-instructions.mdc"
        echo "  ✅ .cursor/rules/agent-instructions.mdc → setup/rules/agent-instructions.mdc"
    fi

    echo ""
    echo "IDE discovery symlinks created successfully."
}

setup_symlinks

if [ "${1}" = "--symlinks-only" ]; then
    echo "==================================================================="
    echo "  Symlinks-only mode complete. Skipping dependency installation."
    echo "==================================================================="
    exit 0
fi

# ─── Dependency check ──────────────────────────────────────────────────────
echo "--- Running dependency diagnostics ---"
python3 "$ROOT_DIR/core/launchers/analyze.py" doctor

# ─── Python dependencies ───────────────────────────────────────────────────
echo ""
echo "--- Installing Python dependencies (Pillow, faster-whisper) ---"
if command -v uv &> /dev/null; then
    uv pip install Pillow faster-whisper 2>/dev/null || true
elif command -v pip3 &> /dev/null; then
    pip3 install Pillow faster-whisper 2>/dev/null || true
fi

echo ""
echo "==================================================================="
echo "  Setup complete! You can now run:"
echo ""
echo "  python3 core/launchers/analyze.py image  <path>"
echo "  python3 core/launchers/analyze.py video  <path>"
echo "  python3 core/launchers/analyze.py website <url>"
echo "  python3 core/launchers/analyze.py route  \"<your prompt>\""
echo "  python3 core/launchers/analyze.py doctor"
echo "==================================================================="
