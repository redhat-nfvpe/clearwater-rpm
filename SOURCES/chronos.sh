#!/bin/bash
set -e

# See: debian/chronos.init.d

NAME=chronos

PIDFILE="/var/run/$NAME/$NAME.pid"

export LD_LIBRARY_PATH="/usr/share/$NAME/lib"

"/usr/bin/$NAME" \
  --pidfile="$PIDFILE"

# Note: --daemon is supported but not needed here
