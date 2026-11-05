#!/usr/bin/env bash
# "Sadece Sigmalar Anlar: Özel Bölüm" derlemesini tek MP4 olarak üretir:
# giriş kartı + her senaryonun başında "SENARYO N" kartı + 5 senaryo + "ÖZEL BÖLÜM SONU" kapanışı.
# Kullanım: bash scripts/render-sigma-ozel.sh [çıktı.mp4]   (THREE_PATH isteğe bağlı)
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${1:-sigmalar-anlar-ozel.mp4}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
R=scripts/render-fps-nerede.cjs
for c in 0 1 2 3 4 5 6; do HTML="sigma-ozel.html?card=$c" node $R "$TMP/c$c.mp4" >/dev/null; done
for v in 1 2 3 4 5; do HTML="sigma-ozel.html?v=$v" node $R "$TMP/v$v.mp4" >/dev/null; done
IN=(); F=""; n=0
for p in c0 c1 v1 c2 v2 c3 v3 c4 v4 c5 v5 c6; do IN+=(-i "$TMP/$p.mp4"); F="$F[$n:v][$n:a]"; n=$((n+1)); done
ffmpeg -v error -y "${IN[@]}" -filter_complex "${F}concat=n=$n:v=1:a=1[v][a]" -map "[v]" -map "[a]" \
  -c:v libx264 -crf 27 -preset slow -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$OUT"
echo "bitti: $OUT"
