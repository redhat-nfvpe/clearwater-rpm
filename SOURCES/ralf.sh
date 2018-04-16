#!/bin/bash

# See: debian/ralf.init.d

NAME=ralf

PIDFILE="/var/run/$NAME/$NAME.pid"

log_directory="/var/log/$NAME"

export LD_LIBRARY_PATH="/usr/share/clearwater/$NAME/lib"

sas_server=0.0.0.0
signaling_dns_server=127.0.0.1
num_http_threads=$(($(grep processor /proc/cpuinfo | wc -l) * 50))
log_level=2

. /etc/clearwater/config

has_content () {
 if [ -d "$1" ]; then
   find "$1" -mindepth 1 -print -quit | grep -q .
   return $?
 fi
 return 1
}

# Work out which features are enabled
if has_content /etc/clearwater/features.d; then
  for file in $(find /etc/clearwater/features.d -type f); do
    [ -r "$file" ] && . "$file"
  done
fi

# Set the destination realm correctly
if [ ! -z "$billing_realm" ]; then
  billing_realm_arg="--billing-realm=$billing_realm"
elif [ ! -z "$home_domain" ]; then
  billing_realm_arg="--billing-realm=$home_domain"
fi

[ "$sas_use_signaling_interface" != Y ] || sas_signaling_if_arg="--sas-use-signaling-interface"

[ -z "$diameter_timeout_ms" ] || diameter_timeout_ms_arg="--diameter-timeout-ms=$diameter_timeout_ms"
[ -z "$ralf_target_latency_us" ] || target_latency_us_arg="--target-latency-us=$ralf_target_latency_us"
[ -z "$ralf_max_tokens" ] || max_tokens_arg="--max-tokens=$ralf_max_tokens"
[ -z "$ralf_init_token_rate" ] || init_token_rate_arg="--init-token-rate=$ralf_init_token_rate"
[ -z "$ralf_min_token_rate" ] || min_token_rate_arg="--min-token-rate=$ralf_min_token_rate"
[ -z "$ralf_max_token_rate" ] || max_token_rate_arg="--max-token-rate=$ralf_max_token_rate"
[ -z "$exception_max_ttl" ] || exception_max_ttl_arg="--exception-max-ttl=$exception_max_ttl"
[ -z "$cdf_identity" ] || billing_peer_arg="--billing-peer=$cdf_identity"
[ -z "$signaling_namespace" ] || namespace_prefix="ip netns exec $signaling_namespace"
[ -z "$local_site_name" ] || local_site_name_arg="--local-site-name=$local_site_name"
[ -z "$chronos_hostname" ] || chronos_hostname_arg="--chronos-hostname=$chronos_hostname"
[ -z "$ralf_chronos_callback_uri" ] || ralf_chronos_callback_uri_arg="--ralf-chronos-callback-uri=$ralf_chronos_callback_uri"
[ -z "$ralf_hostname" ] || ralf_hostname_arg="--ralf-hostname=$ralf_hostname"
[ -z "$http_acr_logging" ] || http_acr_logging_arg="--http-acr-logging"

EXTRA_ARGS=
[ "$http_blacklist_duration" = "" ]     || EXTRA_ARGS="$EXTRA_ARGS --http-blacklist-duration=$http_blacklist_duration"
[ "$diameter_blacklist_duration" = "" ] || EXTRA_ARGS="$EXTRA_ARGS --diameter-blacklist-duration=$diameter_blacklist_duration"
[ "$astaire_blacklist_duration" = "" ]  || EXTRA_ARGS="$EXTRA_ARGS --astaire-blacklist-duration=$astaire_blacklist_duration"
[ "$dns_timeout" = "" ]                 || EXTRA_ARGS="$EXTRA_ARGS --dns-timeout=$dns_timeout"

$namespace_prefix \
"/usr/share/clearwater/bin/$NAME" \
  --localhost="$local_ip" \
  "$local_site_name_arg" \
  --http="$local_ip" \
  --http-threads="$num_http_threads" \
  --session-stores="$ralf_session_store" \
  --access-log="$log_directory" \
  --dns-servers="$signaling_dns_server" \
  --log-file="$log_directory" \
  --log-level="$log_level" \
  "$chronos_hostname_arg" \
  "$ralf_chronos_callback_uri_arg" \
  "$ralf_hostname_arg" \
  "$http_acr_logging_arg" \
  "$billing_realm_arg" \
  "$billing_peer_arg" \
  "$diameter_timeout_ms_arg" \
  "$target_latency_us_arg" \
  "$max_tokens_arg" \
  "$init_token_rate_arg" \
  "$min_token_rate_arg" \
  "$max_token_rate_arg" \
  "$exception_max_ttl_arg" \
  "$sas_signaling_if_arg" \
  --sas="$sas_server,$NAME@$public_hostname" \
  $EXTRA_ARGS \
  --pidfile="$PIDFILE" \
  --daemon
