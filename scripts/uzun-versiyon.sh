#!/usr/bin/env bash
# Abdullah osuruk/kaka serisinin tüm bölümlerini yapılış sırasına göre, bölüm kartlarıyla tek videoda birleştirir.
# Kullanım: bash scripts/uzun-versiyon.sh 16x9|9x16
set -euo pipefail
cd "$(dirname "$0")/.."
MODE="${1:-16x9}"
if [ "$MODE" = 16x9 ]; then W=1280; H=720; FS=64; FS2=34; OUT=abdullah-osurdu-uzun.mp4; SUF=""; else W=1080; H=1920; FS=80; FS2=40; OUT=abdullah-osurdu-uzun-9x16.mp4; SUF="-9x16"; fi
FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
BOL=(osuruk kaka disiplin aranan birakiyor biyolojik-silah birakiyor-absurt yakalandi keciore basur)
ADI=("ABDULLAH HER YERDE OSURUYOR" "OSURUP SIÇIYOR" "DİSİPLİNLİK" "ARANAN ADAM" "SIÇIP BIRAKIYOR" "BİYOLOJİK SİLAH" "SIÇIP BIRAKIYOR 2" "YAKALANDI" "KEÇİÖREN KAKAYA BOĞULDU" "BASUR PATLADI")
card() { # $1 çıktı, $2 süre, $3 üst yazı, $4 alt yazı
  printf '%s' "$3" > "$TMP/t1.txt"; printf '%s' "$4" > "$TMP/t2.txt"
  ffmpeg -v error -y -f lavfi -i "color=c=0x1a1008:s=${W}x${H}:r=30:d=$2" -f lavfi -i "anullsrc=r=44100:cl=stereo" -t "$2" \
    -vf "drawtext=fontfile=$FONT:textfile=$TMP/t1.txt:fontsize=$FS:fontcolor=0xffd84a:borderw=5:bordercolor=black:x=(w-tw)/2:y=h/2-th-10:alpha='min(1,t*3)',drawtext=fontfile=$FONT:textfile=$TMP/t2.txt:fontsize=$FS2:fontcolor=white:borderw=3:bordercolor=black:x=(w-tw)/2:y=h/2+30:alpha='min(1,max(0,(t-.3)*3))',format=yuv420p" \
    -c:v libx264 -crf 20 -preset veryfast -c:a aac -b:a 160k -shortest "$1"; }
card "$TMP/c00.mp4" 3.5 "ABDULLAH OSURDU" "UZUN VERSİYON · 10 BÖLÜM"
LIST=("$TMP/c00.mp4")
for i in "${!BOL[@]}"; do n=$((i+1)); f="${BOL[$i]}"
  card "$TMP/c$n.mp4" 2.5 "BÖLÜM $n" "${ADI[$i]}"; LIST+=("$TMP/c$n.mp4")
  src="$f$SUF.mp4"; [ -f "$src" ] || src="$f.mp4"
  sw=$(ffprobe -v error -select_streams v -show_entries stream=width -of csv=p=0 "$src"); sh=$(ffprobe -v error -select_streams v -show_entries stream=height -of csv=p=0 "$src")
  if [ "$MODE" = 16x9 ] && [ "$sh" -gt "$sw" ]; then
    VF="[0:v]split=2[a][b];[a]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},boxblur=24:4,eq=brightness=-0.12[bg];[b]scale=-2:${H}[fg];[bg][fg]overlay=(W-w)/2:0,fps=30,setsar=1,format=yuv420p[v]"
  else VF="[0:v]scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2,fps=30,setsar=1,format=yuv420p[v]"; fi
  ffmpeg -v error -y -i "$src" -filter_complex "$VF;[0:a]aresample=44100,aformat=channel_layouts=stereo[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 21 -preset veryfast -c:a aac -b:a 160k "$TMP/b$n.mp4"
  LIST+=("$TMP/b$n.mp4")
done
card "$TMP/cz.mp4" 3.5 "SON" "abdullah hâlâ uzayda · koku hâlâ geçmedi"; LIST+=("$TMP/cz.mp4")
: > "$TMP/list.txt"; for p in "${LIST[@]}"; do echo "file '$p'" >> "$TMP/list.txt"; done
ffmpeg -v error -y -f concat -safe 0 -i "$TMP/list.txt" -c:v libx264 -crf 22 -preset medium -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -movflags +faststart "$OUT"
echo "bitti: $OUT"
