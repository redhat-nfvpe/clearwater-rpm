#!/bin/bash
set -e

# See: debian/bono.init.d

NAME=bono

PIDFILE="/var/run/$NAME/$NAME.pid"

log_directory="/var/log/$NAME"

export MIBS=
export LD_LIBRARY_PATH=/usr/share/clearwater/sprout/lib

# Set up defaults and then pull in the settings for this node
sas_server=0.0.0.0
signaling_dns_server=127.0.0.1
bono_alias_list=

. /etc/clearwater/config

# Set the upstream hostname to the sprout hostname only if it hasn't
# already been set (we have to do this after dotting in the config
# as the sprout_hostname value comes from the config file)
[ -n "$upstream_hostname" ] || upstream_hostname="icscf.$sprout_hostname"
[ -n "$upstream_port" ] || upstream_port=5052

# Set up defaults for user settings then pull in any overrides.
# Bono doesn't need multi-threading, so set the number of threads to
# the number of cores.  The number of PJSIP threads must be 1, as its
# code is not multi-threadable.
num_worker_threads=$(grep processor /proc/cpuinfo | wc -l)
log_level=2
upstream_connections=50
upstream_recycle_connections=600
[ -r /etc/clearwater/user_settings ] && . /etc/clearwater/user_settings

IBCF_ENABLED=Y

has_content ()
{
 if [ -d "$1" ]; then
   find "$1" -mindepth 1 -print -quit | grep -q .
   return $?
 fi
 return 1
}

# Work out which features are enabled
if has_content /etc/clearwater/features.d/; then
  for file in $(find /etc/clearwater/features.d/ -type f); do
    [ -r "$file" ] && . "$file"
  done
fi

if [ "$IBCF_ENABLED" = Y ]; then
  [ -z "$trusted_peers" ] || ibcf_arg="--ibcf=$trusted_peers"
  [ -z "$ibcf_domain" ] || bono_alias_list="$bono_alias_list,$ibcf_domain"
fi

[ -z "$ralf_hostname" ] || ralf_arg="--ralf=$ralf_hostname"
# cdf_identity is the correct option for billing cdf.  For historical reasons, we also allow billing_cdf.
[ -z "$cdf_identity" ] || billing_cdf_arg="--billing-cdf=$cdf_identity"
[ -z "$billing_cdf" ] || billing_cdf_arg="--billing-cdf=$billing_cdf"
[ -z "$target_latency_us" ] || target_latency_us_arg="--target-latency-us=$target_latency_us"
[ -z "$max_tokens" ] || max_tokens_arg="--max-tokens=$max_tokens"
[ -z "$init_token_rate" ] || init_token_rate_arg="--init-token-rate=$init_token_rate"
[ -z "$min_token_rate" ] || min_token_rate_arg="--min-token-rate=$min_token_rate"
[ -z "$exception_max_ttl" ] || exception_max_ttl_arg="--exception-max-ttl=$exception_max_ttl"

EXTRA_ARGS=        
[ "$additional_home_domains" = "" ] || EXTRA_ARGS="$EXTRA_ARGS --additional-domains=$additional_home_domains"
[ "$sip_blacklist_duration" = "" ]  || EXTRA_ARGS="$EXTRA_ARGS --sip-blacklist-duration=$sip_blacklist_duration"
[ "$http_blacklist_duration" = "" ] || EXTRA_ARGS="$EXTRA_ARGS --http-blacklist-duration=$http_blacklist_duration"
[ "$sip_tcp_connect_timeout" = "" ] || EXTRA_ARGS="$EXTRA_ARGS --sip-tcp-connect-timeout=$sip_tcp_connect_timeout"
[ "$sip_tcp_send_timeout" = "" ]    || EXTRA_ARGS="$EXTRA_ARGS --sip-tcp-send-timeout=$sip_tcp_send_timeout"
[ "$pbx_service_route" = "" ]       || EXTRA_ARGS="$EXTRA_ARGS --pbx-service-route=$pbx_service_route"
[ "$pbxes" = "" ]                   || EXTRA_ARGS="$EXTRA_ARGS --non-registering-pbxes=$pbxes"

# TODO: needs root
#/usr/share/clearwater/bin/run-in-signaling-namespace \

"/usr/share/clearwater/bin/$NAME" \
  --domain="$home_domain" \
  --localhost="$local_ip,$public_hostname" \
  --alias="$public_ip,$public_hostname,$bono_alias_list" \
  --pcscf=5060,5058 \
  --webrtc-port=5062 \
  --routing-proxy="$upstream_hostname,$upstream_port,$upstream_connections,$upstream_recycle_connections" \
  "$ralf_arg" \
  --sas="$sas_server,$NAME@$public_hostname" \
  --dns-server="$signaling_dns_server" \
  --worker-threads="$num_worker_threads" \
  --analytics="$log_directory" \
  --log-file="$log_directory" \
  --log-level="$log_level" \
  "$target_latency_us_arg" \
  "$max_tokens_arg" \
  "$init_token_rate_arg" \
  "$min_token_rate_arg" \
  "$ibcf_arg" \
  "$billing_cdf_arg" \
  "$exception_max_ttl_arg" \
  $EXTRA_ARGS \
  --pidfile="$PIDFILE"

# Note: --daemon is supported but not needed here
