#!/bin/bash
set -e

# See: debian/ellis.init.d

NAME=ellis

log_level=2

. /etc/clearwater/config

# PID file is configured in /usr/share/clearwater/ellis/local_settings.py

"/usr/share/clearwater/$NAME/env/bin/python" \
  -m metaswitch.$NAME.main \
  --log-level $log_level \
  --background

# Wait for PID file to be written so that systemd doesn't emit the (harmless) warning:
# "Supervising process which is not our child"
sleep 1
