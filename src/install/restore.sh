echo "restore"
USER=root
PASSWD=Qb0Xj7vmKNJ7+Xv
mysql -u${USER} -p${PASSWD} ugc < ugc-table-data.sql
mysql -u${USER} -p${PASSWD} ugc < ugc-stored-procs.sql
