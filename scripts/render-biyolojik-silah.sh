#!/usr/bin/env bash
# "Biyolojik Silah" dikey (9:16) videosunu üretir: 720x1280 render + Speko anlatımı + 1080x1920 ölçekleme.
# Kullanım: bash scripts/render-biyolojik-silah.sh [çıktı.mp4]   (THREE_PATH isteğe bağlı)
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${1:-biyolojik-silah.mp4}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
HTML=biyolojik-silah.html VW=720 VH=1280 node scripts/render-fps-nerede.cjs "$TMP/ham.mp4" >/dev/null
ffmpeg -v error -y -i assets/anlatim/biyolojik-silah-anlatim.mp3 "$TMP/anlatim.wav"
(cd scripts/anlatim-biyolojik-silah && python3 mix.py "$TMP/mix.mp4" "$TMP/ham.mp4" "$TMP/anlatim.wav")
ffmpeg -v error -y -i "$TMP/mix.mp4" -vf "scale=1080:1920:flags=lanczos,format=yuv420p" -c:v libx264 -crf 21 -preset slow -c:a copy -movflags +faststart "$OUT"
echo "bitti: $OUT"
