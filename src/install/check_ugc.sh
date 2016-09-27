WORK_DIR=/home/spider/spider-man/ugc
exist=`/bin/ps -ef|/bin/grep "manage.py"|/bin/grep -v "grep"| /bin/grep "runserver 0.0.0.0:7777" | /usr/bin/wc -l`
/bin/echo `date`
if [ $exist -gt 0 ]
then
    /bin/echo "ugc server is already running! exit!"
    exit 0
fi
cd $WORK_DIR
/bin/echo "start server in $WORK_DIR"
python=/usr/bin/python
echo nohup $python manage.py  runserver 0.0.0.0:7777
nohup $python manage.py  runserver 0.0.0.0:7777  > /dev/null 2>&1 &
exit 0
