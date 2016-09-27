#/bin/sh

build()
{
   make clean -C $1
   make -C $1 flags=-g
}


build ./util/
build ./http/
build ./config/
build ./mongo_mgr/
build ./ctrl/
build ./service/
build ./

