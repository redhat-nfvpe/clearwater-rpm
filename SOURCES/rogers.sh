#!/bin/bash
set -e

# See: debian/rogers.init.d

NAME=rogers

PIDFILE="/var/run/$NAME/$NAME.pid"

export LD_LIBRARY_PATH="/usr/share/clearwater/$NAME/lib"

log_level=2
. /etc/clearwater/config

if [ -n "$signaling_namespace" ]; then
  namespace_prefix="ip netns exec $signaling_namespace"
fi

$namespace_prefix \
"/usr/share/clearwater/bin/$NAME" \
--cluster-settings-file=/etc/clearwater/cluster_settings \
--log-file="/var/log/$NAME" \
--log-level="$log_level" \
--pidfile="$PIDFILE" &

# Note: we will use "&" instead of "--daemon" here because systemd expects a fork

# Wait for PID file to be written so that systemd doesn't emit the (harmless) warning:
# "Supervising process which is not our child"
sleep 2
