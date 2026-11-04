#!/usr/bin/env bash
# "Sigmalar anladı" derlemesini tek MP4 olarak üretir:
# giriş kartı + her senaryonun başında "SENARYO N" kartı + 5 senaryo.
# Kullanım: bash scripts/render-sigmalar.sh [çıktı.mp4]   (THREE_PATH isteğe bağlı)
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${1:-sigmalar-anladi.mp4}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
R=scripts/render-fps-nerede.cjs
HTML="sigma.html?card=0" node $R "$TMP/c0.mp4"
for v in 1 2 3 4 5; do
  HTML="sigma.html?card=$v" node $R "$TMP/c$v.mp4"
  HTML="sigma.html?v=$v" node $R "$TMP/v$v.mp4"
done
IN=(); F=""; n=0
for p in c0 c1 v1 c2 v2 c3 v3 c4 v4 c5 v5; do IN+=(-i "$TMP/$p.mp4"); F="$F[$n:v][$n:a]"; n=$((n+1)); done
ffmpeg -v error -y "${IN[@]}" -filter_complex "${F}concat=n=$n:v=1:a=1[v][a]" -map "[v]" -map "[a]" \
  -c:v libx264 -crf 27 -preset slow -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$OUT"
echo "bitti: $OUT"
