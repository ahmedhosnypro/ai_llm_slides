#!/usr/bin/env bash
# Global gate for vision-model calls: at most 16 concurrent invocations fleet-wide
# (founder directive 2026-10-09: 2 -> 8 verified healthy (zero aborts/garbage,
# ~1 transcript per 2 min), then 8 -> 16. The localhost:17844 gateway is shared).
# Usage: 16_vision_gate.sh <command> [args...]
set -u
LOCKDIR="${TMPDIR:-/tmp}"
for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  exec 9>>"$LOCKDIR/ir_vision_gate_$i.lock"
  if flock -n 9; then
    "$@"
    rc=$?
    flock -u 9
    exit $rc
  fi
  exec 9>&-
done
# all slots busy — block on slot 0
exec 9>>"$LOCKDIR/ir_vision_gate_0.lock"
flock 9
"$@"
rc=$?
flock -u 9
exit $rc
