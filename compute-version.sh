#!/usr/bin/env bash
# Compute and optionally update the project version
# Usage: ./compute-version.sh [--ci] [--update]
#   --ci      Read bump type from CHANGELOG.md <!-- bump: TYPE --> comment
#   --update  Write the new version to VERSION file

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not found" >&2
    exit 1
fi

exec python3 "$SCRIPT_DIR/compute_version.py" "$@"
