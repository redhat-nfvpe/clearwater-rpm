#!/bin/bash
set -e

# See: debian/memento.init.d

NAME=memento

PIDFILE="/var/run/$NAME/$NAME.pid"

# Set up defaults and then pull in the settings for this node.
sas_server=0.0.0.0
local num_cpus=$(nproc)
num_http_threads=$num_cpus
num_http_worker_threads=$(( $num_cpus * 50 ))

. /etc/clearwater/config

homestead_http_name=$(/usr/share/clearwater/bin/bracket-ipv6-address "$hs_hostname")

# Set up a default cluster_settings file if it does not exist.
[ -f /etc/clearwater/cluster_settings ] || echo "servers=$local_ip:11211" > /etc/clearwater/cluster_settings

# Set up defaults for user settings then pull in any overrides.
log_level=2
[ -r /etc/clearwater/user_settings ] && . /etc/clearwater/user_settings

has-content ()
{
 if [ -d "$1" ]; then
   find "$1" -mindepth 1 -print -quit | grep -q .
   return $?
 fi
 return 1
}

# Work out which features are enabled
if has-content /etc/clearwater/features.d/; then
  for file in $(find /etc/clearwater/features.d/ -type f); do
    [ -r "$file" ] && . "$file"
  done
fi

[ -z "$memento_target_latency_us" ] || target_latency_us_arg="--target-latency-us $memento_target_latency_us"
[ -z "$memento_max_tokens" ] || max_tokens_arg="--max-tokens $memento_max_tokens"
[ -z "$memento_init_token_rate" ] || init_token_rate_arg="--init-token-rate $memento_init_token_rate"
[ -z "$memento_min_token_rate" ] || min_token_rate_arg="--min-token-rate $memento_min_token_rate"
[ -z "$memento_max_token_rate" ] || max_token_rate_arg="--max-token-rate $memento_max_token_rate"
[ -z "$signaling_namespace" ] || namespace_prefix="ip netns exec $signaling_namespace"
[ -z "$exception_max_ttl" ] || exception_max_ttl_arg="--exception-max-ttl $exception_max_ttl"
[ -z "$memento_api_key" ] || api_key_arg="--api-key $memento_api_key"
[ -z "$cassandra_hostname" ] || cassandra_arg="--cassandra=$cassandra_hostname"
[ -z "$memento_auth_store" ] || astaire_arg="--astaire=$memento_auth_store"

EXTRA_ARGS=
[ "$http_blacklist_duration" = "" ]       || EXTRA_ARGS="$EXTRA_ARGS --http-blacklist-duration=\"$http_blacklist_duration\""
[ "$astaire_blacklist_duration" = "" ]    || EXTRA_ARGS="$EXTRA_ARGS --astaire-blacklist-duration=\"$astaire_blacklist_duration\""

$namespace_prefix \
"/usr/share/clearwater/bin/$NAME" \
  --localhost "$local_ip" \
  --http "$local_ip" \
  --http-threads "$num_http_threads" \
  --http-worker-threads "$num_http_worker_threads" \
  --homestead-http-name "$homestead_http_name" \
  --home-domain "$home_domain" \
  --access-log "$log_directory" \
  "$cassandra_arg" \
  "$astaire_arg" \
  "$target_latency_us_arg" \
  "$max_tokens_arg" \
  "$init_token_rate_arg" \
  "$min_token_rate_arg" \
  "$max_token_rate_arg" \
  "$exception_max_ttl_arg" \
  --log-file "$log_directory" \
  --log-level "$log_level" \
  --sas "$sas_server,$NAME@$public_hostname" \
  "$api_key_arg" \
  $EXTRA_ARGS \
  --pidfile="$PIDFILE"

# Note: --daemon is supported but not needed here
