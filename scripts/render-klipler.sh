#!/usr/bin/env bash
# 3 şarkının kliplerini (MP4) ve şarkıların kendisini (MP3) üretir.
# Kullanım: bash scripts/render-klipler.sh   (THREE_PATH isteğe bağlı)
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p klipler
NAMES=(jenny-phonk 700-fps aura-sonsuz)
for s in 1 2 3; do
  n=${NAMES[$((s-1))]}
  HTML="klipler.html?s=$s" node scripts/render-fps-nerede.cjs "klipler/$n.mp4" >/dev/null
  ffmpeg -v error -y -i "klipler/$n.mp4" -vn -c:a libmp3lame -b:a 192k "klipler/$n.mp3"
  echo "bitti: klipler/$n.mp4 + .mp3"
done
