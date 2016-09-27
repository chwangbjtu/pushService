#!/bin/bash

log_dir="/var/log/scrapyd"
run_dir="/var/run/scrapyd"
conf_dir="/etc/scrapyd"
log_file="scrapyd.log"
pid_file="scrapyd.pid"
conf_file="scrapyd.conf"
default_conf="default_"$conf_file
SCRAPYD="scrapyd"

init() {
    which $SCRAPYD >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "$SCRAPYD not found"
        exit 1
    fi

    mkdir -p $log_dir
    mkdir -p $run_dir
    mkdir -p $conf_dir

    cp $default_conf $conf_dir"/"$conf_file
    sed -i "s,\(^eggs_dir.*=\).*,\1 $run_dir\/eggs,g" $conf_dir"/"$conf_file
    sed -i "s,\(^logs_dir.*=\).*,\1 $log_dir,g" $conf_dir"/"$conf_file
    sed -i "s,\(^items_dir.*=\).*,\1 $run_dir\/items,g" $conf_dir"/"$conf_file
    sed -i "s,\(^dbs_dir.*=\).*,\1 $run_dir\/dbs,g" $conf_dir"/"$conf_file
}

status() {
    if [ -f $run_dir"/"$pid_file ]; then
        pid=`cat $run_dir"/"$pid_file`
        ps -p $pid >/dev/null 2>&1
        if [ $? -ne 0 ]; then
            echo "$SCRAPYD not running"
            return 1
        else
            echo "$SCRAPYD running"
            return 0
        fi
    else
        echo "$SCRAPYD not running"
        return 1
    fi
}

start() {
    status >/dev/null 2>&1
    if [ $? -eq 1 ]; then
        nohup $SCRAPYD --pidfile=$run_dir"/"$pid_file -l $log_dir"/"$log_file  >/dev/null 2>&1 &
        echo "$SCRAPYD started"
    else
        echo "$SCRAPYD already running"
    fi
}

stop() {
    killall $SCRAPYD >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "$SCRAPYD not running"
    else
        echo "$SCRAPYD stopped"
    fi
}

restart() {
    stop
    start
}

case "$1" in
    init)
    init 
    ;;
    start)
    start
    ;;
    stop)
    stop
    ;;
    restart)
    restart
    ;;
    status)
    status
    ;;
    *)
	echo "Usage: $0 {start|stop|restart|reload|force-reload|status|cron|condrestart|try-restart}"
    exit 1
esac

exit $?
