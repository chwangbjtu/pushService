echo "back-up"
USER=root
#PASSWD=Qb0Xj7vmKNJ7+Xv
PASSWD=rz33dpsk
mkdir ./backup/
mysqldump -u${USER} -p${PASSWD} -d --add-drop-table ugc > ./backup/ugc-table-init.sql
mysqldump -u${USER} -p${PASSWD} -ntd -R ugc > ./backup/ugc-stored-procs.sql
mysqldump -u${USER} -p${PASSWD} ugc > ./backup/ugc-table-data.sql

#ugc: admin/adminugc54321
#mysql: root
#超级用户：root 
#密码：Qb0Xj7vmKNJ7+Xv

