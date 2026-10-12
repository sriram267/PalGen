#!/usr/bin/env bash
# Universal Multimodal Analyzer Menu Launcher (macOS/Linux)
set -e

echo "==================================================================="
echo "            UNIVERSAL MULTIMODAL END-TO-END ANALYZER"
echo "==================================================================="
echo ""
echo "Select an action:"
echo "  [1] Analyze Image or Document (PNG, JPG, WebP, PDF)"
echo "  [2] Analyze Video or Screencast (.mp4, .mov, .webm)"
echo "  [3] Analyze Website or Web App (localhost or live URL)"
echo "  [4] Run System Doctor (Verify Installed Binaries)"
echo "  [5] Exit"
echo ""
read -p "Enter choice (1-5): " CHOICE

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$CHOICE" in
  1)
    read -p "Enter or drag-and-drop image path: " IMG
    IMG=$(echo "$IMG" | tr -d "'\"")
    python3 "$DIR/analyze.py" image "$IMG"
    ;;
  2)
    read -p "Enter or drag-and-drop video path: " VID
    VID=$(echo "$VID" | tr -d "'\"")
    python3 "$DIR/analyze.py" video "$VID"
    ;;
  3)
    read -p "Enter website URL (e.g. http://localhost:5173 or https://example.com): " URL
    python3 "$DIR/analyze.py" website "$URL"
    ;;
  4)
    python3 "$DIR/analyze.py" doctor
    ;;
  5)
    exit 0
    ;;
  *)
    echo "Invalid choice."
    ;;
esac
