echo "alter store engine"
USER=root
#PASSWD=Qb0Xj7vmKNJ7+Xv
PASSWD=rz33dpsk
echo "remove history [ugc_video/ugc_file/ugc_dat] before 2014.4.15..."
mysql -u${USER} -p${PASSWD} ugc < ugc-remove-history-in-ugc-file-video-dat.sql
echo "alter ugc_video definition, alter task_id to 32 varchar and indexed ... "
mysql -u${USER} -p${PASSWD} ugc < ugc-alter-task-id-in-ugc-video.sql
echo "alter stored procs [proc_add_taskid_tid] whichs add task id in ugc_video ... "
mysql -u${USER} -p${PASSWD} ugc < ugc-add-task-id-in-ugc-video.sql
echo "ok"
