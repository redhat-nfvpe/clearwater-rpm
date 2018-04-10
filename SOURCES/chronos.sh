#!/bin/bash

# See: debian/chronos.init.d

NAME=chronos

PIDFILE="/var/run/$NAME/$NAME.pid"

export LD_LIBRARY_PATH="/usr/share/$NAME/lib"

"/usr/bin/$NAME" \
  --daemon \
  --pidfile="$PIDFILE"
