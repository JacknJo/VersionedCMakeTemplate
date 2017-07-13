#!/bin/bash

RESULT=`find /etc -maxdepth 0 -name '.*-release'`
#echo $RESULT
if [ -f /etc/lsb-release ]; then
#              get all dist info    extract dist name              replace spaces with hyphens   add if OS is 32 or 64 bit
	DIST_INFO=`cat /etc/*-release | sed -nre 's/DISTRIB_DESCRIPTION=\"(.*)\"/\1/p' | sed -nre 's/ /-/p'`
	DIST_INFO=${DIST_INFO}_`uname -m`
else
	echo test
	DIST_NAME=`lsb_release -a 2> /dev/null | sed -nre 's/Distributor ID:[ \t](.*)/\1/p'`
	DIST_VERSION=`lsb_release -a 2> /dev/null | sed -nre 's/Release:[ \t]([0-9].[0-9]).*/\1/p'`
	DIST_INFO=$DIST_NAME-$DIST_VERSION
fi
echo -n $DIST_INFO
