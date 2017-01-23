#!/bin/bash

progname=OpenVPN_client
lockfile=/var/lock/subsys/openvpnclient
prog="/usr/bin/python "$(cd $(dirname $0) && pwd)"/vpnsearchconnect.py"

case "$1" in
  start)
        if [ -e $lockfile ]; then
            echo -n $"VPN connection is existing."
        else
            echo -n $"Starting $progname: "
            $prog $2
            if [ "$?" -eq 0 ]; then
                touch $lockfile
            fi
        fi
	;;
  stop)
        echo -n $"Stopping $progname: "
        rm -f $lockfile
        proc=`ps alx | grep [o]penvpn | awk '{print $3}'`
        kill $proc
	;;
  *)
 	echo $"Usage: $0 {start|stop}"
	exit 1
esac

exit $RETVAL
