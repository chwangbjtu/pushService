WORK_DIR=/home/spider/spider-man/maze_service
exist=`/bin/netstat -nlp | /bin/grep  '0.0.0.0:6809' |/bin/grep -v "grep"|/usr/bin/wc -l`
/bin/echo `date`
if [ $exist -gt 0 ]
then
    /bin/echo "maze server is already running! exit!"
    exit 0
fi
cd $WORK_DIR
/bin/echo "start server in $WORK_DIR"
python=/usr/bin/python
echo nohup $python maze_server.py 
nohup $python maze_server.py  > /dev/null 2>&1 &
exit 0
