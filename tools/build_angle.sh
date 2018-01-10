#!/bin/sh

if [ "$1" == "" ]
then
  echo 'usage: build_angle.sh <Debug|Release>'
  exit 1
fi

CONFIG=$1

if [ ! -d depot_tools ]
then
  git clone https://chromium.googlesource.com/chromium/tools/depot_tools
fi

PATH=$PATH:`pwd`/depot_tools

if [ ! -d node_modules/angle/src ]
then
  cd node_modules
  rm -rf angle
  git clone https://github.com/dfoody/angle.git
  cd ..
fi

cd node_modules/angle

if [ ! -f .gclient ]
then
  python scripts/bootstrap.py
  gclient sync
  git checkout master
fi

if [ ! -f out/$CONFIG/build.ninja ]
then
  gn gen out/$CONFIG
fi

ninja -C out/$CONFIG
