#!/bin/bash
set -e

# See: debian/clearwater-cluster-manager.init.d

NAME=clearwater-cluster-manager

PIDFILE="/var/run/$NAME/$NAME.pid"

if [ -e /etc/clearwater/no_cluster_manager ]; then
  echo "/etc/clearwater/no_cluster_manager exists, not starting cluster manager"
  exit 2
fi

local_site_name=site1
remote_site_name=
remote_cassandra_seeds=
signaling_namespace=
etcd_key=clearwater
etcd_cluster_key=
log_level=3
log_directory="/var/log/$NAME"
cluster_manager_enabled=Y

# This sets up $uuid - it's created by /usr/share/clearwater/infrastructure/scripts/node_identity
. /etc/clearwater/node_identity

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
--mgmt-local-ip="${management_local_ip:-$local_ip}" \
--sig-local-ip="$local_ip" \
--local-site="$local_site_name" \
--remote-site="$remote_site_name" \
--remote-cassandra-seeds="$remote_cassandra_seeds" \
--signaling-namespace="$signaling_namespace" \
--uuid="$uuid" \
--etcd-key="$etcd_key" \
--etcd-cluster-key="$etcd_cluster_key" \
--cluster-manager-enabled="$cluster_manager_enabled" \
--log-level="$log_level" \
--log-directory="$log_directory" \
--pidfile="$PIDFILE"

# Wait for PID file to be written so that systemd doesn't emit the (harmless) warning:
# "Supervising process which is not our child"
sleep 2
