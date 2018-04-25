#!/bin/bash
set -e

# See: debian/restund.init.d

NAME=restund

log_directory="/var/log/$NAME"

export LD_LIBRARY_PATH="/usr/share/clearwater/$NAME/lib"

"/usr/share/clearwater/bin/$NAME" \
  -f "/etc/clearwater/$NAME.conf"
