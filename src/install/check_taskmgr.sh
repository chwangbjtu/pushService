WORK_DIR=/home/spider/spider-man/cloud_taskmgr
exist=`/bin/netstat -nlp | /bin/grep  '0.0.0.0:6600'|/bin/grep -v "grep"|/usr/bin/wc -l`
/bin/echo `date`
if [ $exist -gt 0 ]
then
    /bin/echo "task manager is already running! exit!"
    exit 0
fi
cd $WORK_DIR
/bin/echo "start server in $WORK_DIR"
python=/usr/bin/python
echo nohup $python cloud_taskmgr.py 
nohup $python cloud_taskmgr.py  > /dev/null 2>&1 &
exit 0
