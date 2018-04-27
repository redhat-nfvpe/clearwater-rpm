#!/bin/bash
set -e

# See: debian/clearwater-queue-manager.init.d

NAME=clearwater-queue-manager

PIDFILE="/var/run/$NAME/$NAME.pid"

local_site_name=site1
etcd_key=clearwater
etcd_cluster_key=unknown
log_level=3
log_directory="/var/log/$NAME"
wait_plugin_complete=Y

has_content ()
{
  test "$(find "$1" -mindepth 1 -maxdepth 1 2> /dev/null)"
}

if has_content /usr/share/clearwater/node_type.d/; then
  . "/usr/share/clearwater/node_type.d/$(ls /usr/share/clearwater/node_type.d | head -n 1)"
fi

. /etc/clearwater/config

if [ -z "$local_ip" ]; then
  echo "/etc/clearwater/local_config not provided, not starting"
  exit 3
fi
  
"/usr/share/clearwater/bin/$NAME" \
--local-ip="${management_local_ip:-$local_ip}" \
--local-site="$local_site_name" \
--log-level="$log_level" \
--log-directory="$log_directory" \
--etcd-key="$etcd_key" \
--node-type="$etcd_cluster_key" \
--wait-plugin-complete="$wait_plugin_complete" \
--pidfile="$PIDFILE"

# Wait for PID file to be written so that systemd doesn't emit the (harmless) warning:
# "Supervising process which is not our child"
sleep 2
