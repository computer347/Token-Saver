#!/usr/bin/env bash
# Token battery runner. Give one or more modes; they run in order.
#   ./run_overnight.sh smoke smoke-build        # first night: prove everything works
#   ./run_overnight.sh pilot pilot-build        # method checks on both suites
#   ./run_overnight.sh full full-build          # everything; re-run the same command to resume
#
# Each case is a fresh, context-free `claude -p` process that gets only its prompt and its arm's rules.
# Ponytail is turned off in your normal setup first and restored on exit (TB_KEEP_PONYTAIL_OFF=1 keeps it off).
set -uo pipefail
cd "$(dirname "$0")"
[ $# -eq 0 ] && set -- smoke
PY="$(command -v python3 || command -v python)"   # Git Bash on Windows usually has only `python`
[ -z "$PY" ] && { echo "Python 3.11+ not found"; exit 1; }
export PYTHONUTF8=1
mkdir -p results
LOG="results/overnight-$(date +%Y%m%d-%H%M).log"
exec > >(tee -a "$LOG") 2>&1

INHIBIT_PID=""
cleanup() {
  "$PY" harness/ponytail.py restore
  [ -n "$INHIBIT_PID" ] && kill "$INHIBIT_PID" 2>/dev/null
}
trap cleanup EXIT

if command -v caffeinate >/dev/null 2>&1; then
  caffeinate -i -w $$ &
elif command -v systemd-inhibit >/dev/null 2>&1; then
  systemd-inhibit --what=idle:sleep --why="token battery" --mode=block sleep 604800 &
  INHIBIT_PID=$!
fi

for MODE in "$@"; do
  echo "== Token battery: $MODE · $(date) =="
  "$PY" harness/preflight.py --mode "$MODE" || { echo "Preflight FAILED for $MODE: see results/preflight.json"; exit 1; }
  "$PY" harness/battery.py --mode "$MODE"
done
"$PY" harness/report.py
echo "== Done $(date). Read results/REPORT.md (and REPORT_<suite>.md, NIGHT_REPORT.md) =="
