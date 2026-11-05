#!/usr/bin/env bash
# "İşte Gerçek Baloncukluk Budur" videosunu tek MP4 olarak üretir:
# giriş kartı + 3 senaryo (her birinin başında SENARYO N kartı) + kapanış kartı.
# Kullanım: bash scripts/render-baloncukluk.sh [çıktı.mp4]   (THREE_PATH isteğe bağlı)
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${1:-gercek-baloncukluk.mp4}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
R=scripts/render-fps-nerede.cjs
for c in 0 1 2 3 4; do HTML="baloncukluk.html?card=$c" node $R "$TMP/c$c.mp4" >/dev/null; done
for v in 1 2 3; do HTML="baloncukluk.html?v=$v" node $R "$TMP/v$v.mp4" >/dev/null; done
IN=(); F=""; n=0
for p in c0 c1 v1 c2 v2 c3 v3 c4; do IN+=(-i "$TMP/$p.mp4"); F="$F[$n:v][$n:a]"; n=$((n+1)); done
ffmpeg -v error -y "${IN[@]}" -filter_complex "${F}concat=n=$n:v=1:a=1[v][a]" -map "[v]" -map "[a]" \
  -c:v libx264 -crf 27 -preset slow -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$OUT"
echo "bitti: $OUT"
