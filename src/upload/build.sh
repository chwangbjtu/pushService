#! /usr/bin/env bash

fun()
{
	(cd $1; make clean; make flags="-O2" >> /dev/null)
}

fun ../../../../Library/funshion/src/netsvc/0.1.4/src
#fun ../../../../../Library/funshion/src/http/0.1.2
fun ../../../../Library/funshion/src/kernel/0.1.2
fun ../../../../Library/funshion/src/timer/0.1.0/src
fun ../../../../Library/funshion/src/logger/0.2.0/src
fun ../../../../Library/funshion/src/msgq/0.1.3/src
fun ../../../../Library/funshion/src/thread/0.1.1/src
#(cd ../../../../common/src/json/0.1.1/; ./build.sh clean)
#(cd ../../../../common/src/json/0.1.1/; ./build.sh make)
#fun ../../../../common/src/http/0.1.3
fun ./http
fun ./common
fun ./util
fun ./info_manager
fun ./receptor
fun ./mgmt
fun ./sync_disk
fun ./visitor
fun ./ctrl
fun .

#rm -rf ../bin/etc
#cp -rf ../etc/ ../bin/etc
