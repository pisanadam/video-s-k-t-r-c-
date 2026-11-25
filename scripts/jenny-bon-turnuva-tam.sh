#!/bin/sh
# Jenny Bon turnuvası (yarı finaller + final) + büyük final (basur) birleşik sürüm
set -e
ffmpeg -y -i jenny-bon-turnuva.mp4 -i jenny-bon-final-basur.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 20 -preset fast -c:a aac -b:a 192k -movflags +faststart jenny-bon-turnuva-tam.mp4
ffmpeg -y -i jenny-bon-turnuva-9x16.mp4 -i jenny-bon-final-basur-9x16.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 22 -preset fast -c:a aac -b:a 192k -movflags +faststart jenny-bon-turnuva-tam-9x16.mp4
