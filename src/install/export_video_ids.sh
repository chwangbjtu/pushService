path=$(dirname "$0")
yestoday=$(date -d "-1days"  +%Y%m%d)

python $path/export_video_ids.py -f /media3/upload_files/videoids_$yestoday.txt
 

