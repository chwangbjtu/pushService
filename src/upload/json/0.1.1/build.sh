#!/bin/sh


compile() {
  cd jsoncpp-src-0.5.0
  scons platform=linux-gcc  -c . 
  scons platform=linux-gcc  
  rm -rf ../src/include/json 
  mkdir -p ../src/include 
  cp include/* ../src/include -rf
  cd ..

  make -C src
}

clean() {
  cd jsoncpp-src-0.5.0
  scons platform=linux-gcc  -c .
  rm -rf ../src/include/json
  cd ..

  make -C src clean
}

case "$1" in 
  make)
    compile > /dev/null
  ;;
  clean)
    clean > /dev/null
  ;;
  *)
  exit 1
esac

