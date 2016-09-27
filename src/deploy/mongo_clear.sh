#!/bin/bash
ps aux|grep cfg-27017|grep -v grep
if [[ $? != 0 ]]
then
    mongod -f /home/yuxj/mongo-cluster/cfg-27017.conf --rest
fi
mongo -u xv -p xv 127.0.0.1:27017/xv -quiet mongo_clear.js
