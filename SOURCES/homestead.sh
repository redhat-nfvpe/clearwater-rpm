#!/bin/bash

# See: debian/homestead.init.d

NAME=homestead

PIDFILE="/var/run/$NAME/$NAME.pid"

log_directory="/var/log/$NAME"

export LD_LIBRARY_PATH="/usr/share/clearwater/$NAME/lib"

# Set up defaults and then pull in any overrides
sas_server=0.0.0.0
hss_hostname=0.0.0.0
signaling_dns_server=127.0.0.1
scscf=5054
impu_cache_ttl=0
max_peers=2
hss_reregistration_time=1800
reg_max_expires=300
log_level=2
num_http_threads=$(($(nproc) * 4))
homestead_cache_threads=$(($(nproc) * 150))

hss_mar_scheme_unknown="Unknown"
hss_mar_scheme_digest="SIP Digest"
hss_mar_scheme_akav1="Digest-AKAv1-MD5"
hss_mar_scheme_akav2="Digest-AKAv2-SHA-256"

. /etc/clearwater/config

if [ -n "$homestead_http_threads" ]; then
  num_http_threads="$homestead_http_threads"
fi

# Derive server_name and sprout_http_name from other settings
if [ -n "$scscf_uri" ]; then
  server_name="$scscf_uri"
elif [ -n "$scscf_prefix" ]; then
  server_name="sip:$scscf_prefix.$sprout_hostname;transport=TCP"
else
  server_name="sip:scscf.$sprout_hostname;transport=TCP"
fi

sprout_http_name="$(/usr/share/clearwater/bin/bracket-ipv6-address "$sprout_hostname"):9888"

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

# Set the destination realm correctly
if [ ! -z "$hss_realm" ]; then
  dest_realm="--dest-realm=$hss_realm"
fi

[ "$sas_use_signaling_interface" != Y ] || sas_signaling_if_arg="--sas-use-signaling-interface"
[ "$request_shared_ifcs" != Y ] || request_shared_ifcs_arg="--request-shared-ifcs"

[ -z "$diameter_timeout_ms" ] || diameter_timeout_ms_arg="--diameter-timeout-ms=$diameter_timeout_ms"
[ -z "$signaling_namespace" ] || namespace_prefix="ip netns exec $signaling_namespace"
[ -z "$homestead_target_latency_us" ] || target_latency_us_arg="--target-latency-us=$homestead_target_latency_us"
[ -z "$homestead_max_tokens" ] || max_tokens_arg="--max-tokens=$homestead_max_tokens"
[ -z "$homestead_init_token_rate" ] || init_token_rate_arg="--init-token-rate=$homestead_init_token_rate"
[ -z "$homestead_min_token_rate" ] || min_token_rate_arg="--min-token-rate=$homestead_min_token_rate"
[ -z "$homestead_max_token_rate" ] || max_token_rate_arg="--max-token-rate=$homestead_max_token_rate"
[ -z "$exception_max_ttl" ] || exception_max_ttl_arg="--exception-max-ttl=$exception_max_ttl"
[ -z "$cassandra_hostname" ] || cassandra_arg="--cassandra=$cassandra_hostname"
[ -z "$local_site_name" ] || local_site_name_arg="--local-site-name=$local_site_name"
[ -z "$homestead_impu_store" ] || impu_store_arg="--impu-store=$homestead_impu_store"        

EXTRA_ARGS=
[ "$http_blacklist_duration" = "" ]     || EXTRA_ARGS="$EXTRA_ARGS --http-blacklist-duration=$http_blacklist_duration"
[ "$diameter_blacklist_duration" = "" ] || EXTRA_ARGS="$EXTRA_ARGS --diameter-blacklist-duration=$diameter_blacklist_duration"
[ "$dns_timeout" = "" ]                 || EXTRA_ARGS="$EXTRA_ARGS --dns-timeout=$dns_timeout"
[ "$astaire_blacklist_duration" = "" ]  || EXTRA_ARGS="$EXTRA_ARGS --astaire-blacklist-duration=$astaire_blacklist_duration"

$namespace_prefix \
"/usr/share/clearwater/bin/$NAME" \
  --localhost="$local_ip" \
  --home-domain="$home_domain" \
  --diameter-conf="/var/lib/$NAME/$NAME.conf" \
  --dns-server="$signaling_dns_server" \
  --http="$local_ip" \
  --http-threads="$num_http_threads" \
  --cache-threads="$homestead_cache_threads" \
  "$cassandra_arg" \
  "$dest_realm" \
  --dest-host="$hss_hostname" \
  --hss-peer="$force_hss_peer" \
  --max-peers="$max_peers" \
  --server-name="$server_name" \
  --impu-cache-ttl="$impu_cache_ttl" \
  --hss-reregistration-time="$hss_reregistration_time" \
  --reg-max-expires="$reg_max_expires" \
  --sprout-http-name="$sprout_http_name" \
  --scheme-unknown="$hss_mar_scheme_unknown" \
  --scheme-digest="$hss_mar_scheme_digest" \
  --scheme-akav1="$hss_mar_scheme_akav1" \
  --scheme-akav2="$hss_mar_scheme_akav2" \
  "$diameter_timeout_ms_arg" \
  "$target_latency_us_arg" \
  "$max_tokens_arg" \
  "$init_token_rate_arg" \
  "$min_token_rate_arg" \
  "$max_token_rate_arg" \
  "$exception_max_ttl_arg" \
  "$sas_signaling_if_arg" \
  "$request_shared_ifcs_arg" \
  "$impu_store_arg" \
  "$local_site_name_arg" \
  --access-log="$log_directory" \
  --log-file="$log_directory" \
  --log-level="$log_level" \
  --sas="$sas_server,$NAME@$public_hostname" \
   $EXTRA_ARGS \
  --pidfile="$PIDFILE"

# Note: --daemon is supported but not needed here
