WORK_DIR=/home/spider/spider-man/maze_service
exist=`/bin/ps -ef|/bin/grep "mysqld_safe"|/bin/grep -v "grep"|/usr/bin/wc -l`
/bin/echo `date`
if [ $exist -gt 0 ]
then
    /bin/echo "mysqld is already running! exit!"
    exit 0
fi
echo nohup /usr/local/mysql/bin/mysqld_safe & 
nohup /usr/local/mysql/bin/mysqld_safe   > /dev/null 2>&1 &
exit 0
