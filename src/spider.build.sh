#!/bin/bash
pkg_name="SpiderMan"
version="0.5.2"
build="04"
arc="64"
path=$(dirname $0)
pkg=$path"/"$pkg_name"-"$version

rm -rf $pkg
mkdir -p $pkg

cp -r $path"/cloud_taskmgr" $pkg
cp -r $path"/maze_service" $pkg
cp -r $path"/flashget" $pkg
cp -r $path"/ugc" $pkg
cp -r $path"/install" $pkg
cp -r $path"/plat" $pkg
cp -r $path"/tool" $pkg

cp -r $path"/crawler/crawler" $pkg
cp -r $path"/data_server/data_server/" $pkg

tar zcf $path"/"$pkg_name"-"$version"."$build"_"$arc".tar.gz" -C $path $pkg_name"-"$version

rm -rf $pkg
