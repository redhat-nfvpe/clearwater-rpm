#!/bin/bash

# See: debian/astaire.init.d

NAME=astaire

PIDFILE="/var/run/$NAME/$NAME.pid"

export LD_LIBRARY_PATH="/usr/share/clearwater/$NAME/lib"

log_level=2
. /etc/clearwater/config

if [ -n "$signaling_namespace" ]; then
  namespace_prefix="ip netns exec $signaling_namespace"
fi

$namespace_prefix \
"/usr/share/clearwater/bin/$NAME" \
  --local-name="$local_ip:11211" \
  --cluster-settings-file=/etc/clearwater/cluster_settings \
  --log-file="/var/log/$NAME" \
  --log-level="$log_level" \
  --daemon \
  --pidfile="$PIDFILE"
