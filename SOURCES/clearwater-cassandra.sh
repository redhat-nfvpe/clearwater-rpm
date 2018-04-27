#!/bin/bash
set -e

# See: clearwater-cassandra/etc/init.d/cassandra.clearwater

NAME=cassandra

PIDFILE="/var/run/$NAME/$NAME.pid"

[ -e /etc/cassandra/cassandra.yaml ] || ( echo "Exiting: cassandra.yaml is missing" && exit 2 )
[ -e /etc/cassandra/cassandra-env.sh ] || ( echo "Exiting: cassandra-env.sh is missing" && exit 2 )

if [ -f /usr/share/clearwater/bin/run-in-signaling-namespace ]; then
  namespace_prefix = /usr/share/clearwater/bin/run-in-signaling-namespace
fi

cassandra_home=$(getent passwd cassandra | awk -F ':' '{ print $6; }')
date=$(date +%s)
heap_dump_f="$cassandra_home/java_$date.hprof"
error_log_f="$cassandra_home/hs_err_$date.log"

$namespace_prefix \
"/usr/sbin/$NAME"
-p "$PIDFILE" \
-H "$heap_dump_f" \
-E "$error_log_f"
