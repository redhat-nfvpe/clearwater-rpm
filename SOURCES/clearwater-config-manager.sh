#!/bin/bash
set -e

# See: debian/clearwater-config-manager.init.d

NAME=clearwater-config-manager

PIDFILE="/var/run/$NAME/$NAME.pid"

if [ -e /etc/clearwater/no_config_manager ]; then
  echo "/etc/clearwater/no_config_manager exists, not starting config manager"
  exit 2
fi

local_site_name=site1
etcd_key=clearwater
log_level=3
log_directory="/var/log/$NAME"
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
  --pidfile="$PIDFILE"
