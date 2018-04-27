#!/bin/bash
set -e

# See: debian/homestead-prov.init.d

NAME=homestead

log_level=2

. /etc/clearwater/config

export CREST_SETTINGS="/usr/share/clearwater/$NAME/local_settings.py"
export PYTHONPATH="/usr/share/clearwater/$NAME/python/packages"

if [ -n "$signaling_namespace" ]; then
  namespace_prefix="ip netns exec $signaling_namespace"
  signaling_opt="--signaling-namespace"
fi

$namespace_prefix \
/usr/share/clearwater/crest/env/bin/python \
-m metaswitch.crest.main \
--worker-processes 1 \
$signaling_opt \
--log-level $log_level \
--background
