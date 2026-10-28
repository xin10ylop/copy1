#!/bin/bash
# setup.sh REPO: unpack the datasets these scripts read into the scratchpad path they hard-code (SP), link the repo where
# the older scripts expect it, and put oprule/options.py's two inputs in SP/oprule (they were not in any archive).
set -euo pipefail
REPO=${1:-/home/user/copy1}
SP=/tmp/claude-0/-home-user-rugsnipe/972c43cf-f494-5af4-b87a-fe32117a83be/scratchpad
bash "$REPO/data/datasets/unpack.sh" dec ext month fp full univ rivalpnl helpers oos refused fails hold
[ -e /home/user/rugsnipe ] || ln -s "$REPO" /home/user/rugsnipe
mkdir -p "$SP/oprule"
cp "$REPO/analysis/research/2026-10-26/oprule/arrival.py" "$SP/oprule/arrival.py"
echo 8ZN71XTdVo8yRovnGLmNgW3Tgniw6A4J3JGLvPD686FP > "$SP/oprule/op8zn.txt"   # 8ZN71X's address, as in data/operators/*.json
