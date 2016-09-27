#!/bin/bash

start() {
        nohup python data_server.py & >/dev/null 2>&1
}

stop() {
        for pid in `ps ax | grep data_server | grep -v grep | awk '{print $1}'`; do kill -9 $pid; done
}

case "$1" in
        start)
        start
        ;;
        stop)
        stop
        ;;
        *)
        echo "Usage: $0 {start|stop}"
        exit 1
esac

exit $?
