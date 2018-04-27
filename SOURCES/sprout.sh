#!/bin/bash
set -e

# See: sprout-base.root/init.d/sprout

# Note: unlike other Clearwater components, the Sprout init script is in the root dir rather than
# the Debian dir

NAME=sprout

PIDFILE="/var/run/$NAME/$NAME.pid"

log_directory="/var/log/$NAME"

export MIBS=

# Set up defaults and then pull in the settings for this node.
sas_server=0.0.0.0
sprout_rr_level=pcscf

# These Sproutlets are enabled by default. They listen on different
# ports to help ensure that requests have a unambiguous Sproutlet
# to route to.
icscf=5052
bgcf=5053
scscf=5054
mmtel=5055

alias_list=
default_session_expires=600
signaling_dns_server=127.0.0.1
blacklisted_scscf_uris=
scscf_node_uri=

# Enable no-ENUM TEL URI translation fallback by default for backwards compatibility
default_tel_uri_translation=Y

# Enable the treatment of originating SIP "user=phone" URIs (that corresponding to global
# phone numbers) as though they were Tel URIs for Identity purposes by default.
enable_orig_sip_to_tel_coerce=Y

# Set up defaults for user settings then pull in any overrides.
# Sprout uses blocking look-up services, so must run multi-threaded.
num_worker_threads=$(($(nproc) * 250))
num_http_threads=$(($(nproc) * 50))

log_level=2
authentication=Y

. /etc/clearwater/config

if [ -n "$sprout_worker_threads" ];
then
  num_worker_threads="$sprout_worker_threads"
fi

if [ -n "$sprout_http_threads" ];
then
  num_http_threads="$sprout_http_threads"
fi

# Calculate the correct homestead latency:
#  - if we have sprout_homestead_timeout_ms set, use that
#  - else:
#    - if we have diameter_timeout_ms set, use 1000 + double that
#    - else use 1200
if [ -z "$sprout_homestead_timeout_ms" ]; then
  if [ -z "$diameter_timeout_ms" ]; then
    sprout_homestead_timeout_ms=1200
  else
    sprout_homestead_timeout_ms=$((diameter_timeout_ms * 2 + 1000))
  fi
fi

MMTEL_SERVICES_ENABLED=Y

has_content ()
{
  test "$(find "$1" -mindepth 1 -maxdepth 1 2> /dev/null)"
}

# Work out which features are enabled
if has_content /etc/clearwater/features.d/; then
  for file in $(find /etc/clearwater/features.d/ -type f); do
    [ -r "$file" ] && . "$file"
  done
fi

[ -z "$enum_server" ] || enum_server_arg="--enum=$enum_server"
[ -z "$enum_suffix" ] || enum_suffix_arg="--enum-suffix=$enum_suffix"
[ -z "$enum_file" ] || enum_file_arg="--enum-file=$enum_file"
[ "$default_tel_uri_translation" != Y ] || default_tel_uri_translation_arg="--default-tel-uri-translation"

if [ $MMTEL_SERVICES_ENABLED = Y ]; then
  [ -z "$xdms_hostname" ] || xdms_hostname_arg="--xdms=$xdms_hostname"
fi

[ -z "$ralf_hostname" ] || ralf_arg="--ralf=$ralf_hostname"

[ "$authentication" != Y ] || authentication_arg="--authentication"

[ "$enforce_user_phone" != Y ] || user_phone_arg="--enforce-user-phone"
[ "$enforce_global_only_lookups" != Y ] || global_only_lookups_arg="--enforce-global-only-lookups"
[ "$override_npdi" != Y ] || override_npdi_arg="--override-npdi"
[ "$force_third_party_reg_body" != Y ] || force_3pr_body_arg="--force-3pr-body"
[ "$sas_use_signaling_interface" != Y ] || sas_signaling_if_arg="--sas-use-signaling-interface"
[ "$disable_tcp_switch" != Y ] || disable_tcp_switch_arg="--disable-tcp-switch"
[ "$apply_fallback_ifcs" != Y ] || apply_fallback_ifcs_arg="--apply-fallback-ifcs"
[ "$reject_if_no_matching_ifcs" != Y ] || reject_if_no_matching_ifcs_arg="--reject-if-no-matching-ifcs"
[ "$http_acr_logging" != Y ] || http_acr_logging_arg="--http-acr-logging"
[ "$enable_orig_sip_to_tel_coerce" != Y ] || enable_orig_sip_to_tel_coerce_arg="--enable-orig-sip-to-tel-coerce"

[ -z "$sprout_target_latency_us" ] || target_latency_us_arg="--target-latency-us=$sprout_target_latency_us"
[ -z "$cass_target_latency_us" ] || cass_target_latency_us_arg="--cass-target-latency-us=$cass_target_latency_us"
[ -z "$sprout_max_tokens" ] || max_tokens_arg="--max-tokens=$sprout_max_tokens"
[ -z "$sprout_init_token_rate" ] || init_token_rate_arg="--init-token-rate=$sprout_init_token_rate"
[ -z "$sprout_min_token_rate" ] || min_token_rate_arg="--min-token-rate=$sprout_min_token_rate"
[ -z "$sprout_max_token_rate" ] || max_token_rate_arg="--max-token-rate=$sprout_max_token_rate"
[ -z "$exception_max_ttl" ] || exception_max_ttl_arg="--exception-max-ttl=$exception_max_ttl"
[ -z "$max_session_expires" ] || max_session_expires_arg="--max-session-expires=$max_session_expires"
[ -z "$local_site_name" ] || local_site_name_arg="--local-site-name=$local_site_name"
[ -z "$sprout_impi_store" ] || impi_store_arg="--impi-store=$sprout_impi_store"
[ -z "$chronos_hostname" ] || chronos_hostname_arg="--chronos-hostname=$chronos_hostname"
[ -z "$sprout_chronos_callback_uri" ] || sprout_chronos_callback_uri_arg="--sprout-chronos-callback-uri=$sprout_chronos_callback_uri"
[ -z "$dummy_app_server" ] || dummy_app_server_arg="--dummy-app-server=$dummy_app_server"
[ -z "$sprout_request_on_queue_timeout" ] || request_on_queue_timeout_arg="--request-on-queue-timeout=$sprout_request_on_queue_timeout"

EXTRA_ARGS=

if [ -n "$reg_max_expires" ]; then
  EXTRA_ARGS="$EXTRA_ARGS --reg-max-expires=$reg_max_expires"
fi

if [ -n "$sub_max_expires" ]; then
  EXTRA_ARGS="$EXTRA_ARGS --sub-max-expires=$sub_max_expires"
fi

if [ -n "$memento_threads" ]; then
  EXTRA_ARGS="$EXTRA_ARGS --memento-threads=$memento_threads"
fi

if [ -n "$max_call_list_length" ]; then
  EXTRA_ARGS="$EXTRA_ARGS --max-call-list-length=$max_call_list_length"
fi

if [ -n "$memento_notify_url" ]; then
  EXTRA_ARGS="$EXTRA_ARGS --memento-notify-url=$memento_notify_url"
fi

if [ -n "$call_list_ttl" ]; then
  EXTRA_ARGS="$EXTRA_ARGS --call-list-ttl=$call_list_ttl"
fi

if [ -n "$memento" ] && [ -n "$cassandra_hostname" ]; then
  EXTRA_ARGS="$EXTRA_ARGS --plugin-option=memento,cassandra,$cassandra_hostname"
fi

# TODO improve this so we don't have to have the same parameters
# repeated for each Sproutlet
[ "$icscf" = "" ]                         || EXTRA_ARGS="$EXTRA_ARGS --icscf=$icscf"
[ "$icscf_prefix" = "" ]                  || EXTRA_ARGS="$EXTRA_ARGS --prefix-icscf=$icscf_prefix"
[ "$icscf_uri" = "" ]                     || EXTRA_ARGS="$EXTRA_ARGS --uri-icscf=$icscf_uri"
[ "$scscf" = "" ]                         || EXTRA_ARGS="$EXTRA_ARGS --scscf=$scscf"
[ "$scscf_prefix" = "" ]                  || EXTRA_ARGS="$EXTRA_ARGS --prefix-scscf=$scscf_prefix"
[ "$scscf_uri" = "" ]                     || EXTRA_ARGS="$EXTRA_ARGS --uri-scscf=$scscf_uri"
[ "$bgcf" = "" ]                          || EXTRA_ARGS="$EXTRA_ARGS --bgcf=$bgcf"
[ "$bgcf_prefix" = "" ]                   || EXTRA_ARGS="$EXTRA_ARGS --prefix-bgcf=$bgcf_prefix"
[ "$bgcf_uri" = "" ]                      || EXTRA_ARGS="$EXTRA_ARGS --uri-bgcf=$bgcf_uri"
[ "$memento" = "" ]                       || EXTRA_ARGS="$EXTRA_ARGS --memento=$memento"
[ "$memento_prefix" = "" ]                || EXTRA_ARGS="$EXTRA_ARGS --prefix-memento=$memento_prefix"
[ "$memento_uri" = "" ]                   || EXTRA_ARGS="$EXTRA_ARGS --uri-memento=$memento_uri"
[ "$gemini" = "" ]                        || EXTRA_ARGS="$EXTRA_ARGS --gemini=$gemini"
[ "$gemini_prefix" = "" ]                 || EXTRA_ARGS="$EXTRA_ARGS --prefix-gemini=$gemini_prefix"
[ "$gemini_uri" = "" ]                    || EXTRA_ARGS="$EXTRA_ARGS --uri-gemini=$gemini_uri"
[ "$cdiv" = "" ]                          || EXTRA_ARGS="$EXTRA_ARGS --cdiv=$cdiv"
[ "$cdiv_prefix" = "" ]                   || EXTRA_ARGS="$EXTRA_ARGS --prefix-cdiv=$cdiv_prefix"
[ "$cdiv_uri" = "" ]                      || EXTRA_ARGS="$EXTRA_ARGS --uri-cdiv=$cdiv_uri"
[ "$mmtel" = "" ]                         || EXTRA_ARGS="$EXTRA_ARGS --mmtel=$mmtel"
[ "$mmtel_prefix" = "" ]                  || EXTRA_ARGS="$EXTRA_ARGS --prefix-mmtel=$mmtel_prefix"
[ "$mmtel_uri" = "" ]                     || EXTRA_ARGS="$EXTRA_ARGS --uri-mmtel=$mmtel_uri"
[ "$mangelwurzel" = "" ]                  || EXTRA_ARGS="$EXTRA_ARGS --mangelwurzel=$mangelwurzel"
[ "$mangelwurzel_prefix" = "" ]           || EXTRA_ARGS="$EXTRA_ARGS --prefix-mangelwurzel=$mangelwurzel_prefix"
[ "$mangelwurzel_uri" = "" ]              || EXTRA_ARGS="$EXTRA_ARGS --uri-mangelwurzel=$mangelwurzel_uri"
[ "$external_icscf_uri" = "" ]            || EXTRA_ARGS="$EXTRA_ARGS --external-icscf=$external_icscf_uri"
[ "$additional_home_domains" = "" ]       || EXTRA_ARGS="$EXTRA_ARGS --additional-domains=$additional_home_domains"
[ "$sip_blacklist_duration" = "" ]        || EXTRA_ARGS="$EXTRA_ARGS --sip-blacklist-duration=$sip_blacklist_duration"
[ "$http_blacklist_duration" = "" ]       || EXTRA_ARGS="$EXTRA_ARGS --http-blacklist-duration=$http_blacklist_duration"
[ "$astaire_blacklist_duration" = "" ]    || EXTRA_ARGS="$EXTRA_ARGS --astaire-blacklist-duration=$astaire_blacklist_duration"
[ "$sip_tcp_connect_timeout" = "" ]       || EXTRA_ARGS="$EXTRA_ARGS --sip-tcp-connect-timeout=$sip_tcp_connect_timeout"
[ "$sip_tcp_send_timeout" = "" ]          || EXTRA_ARGS="$EXTRA_ARGS --sip-tcp-send-timeout=$sip_tcp_send_timeout"
[ "$dns_timeout" = "" ]                   || EXTRA_ARGS="$EXTRA_ARGS --dns-timeout=$dns_timeout"
[ "$session_continued_timeout_ms" = "" ]  || EXTRA_ARGS="$EXTRA_ARGS --session-continued-timeout=$session_continued_timeout_ms"
[ "$session_terminated_timeout_ms" = "" ] || EXTRA_ARGS="$EXTRA_ARGS --session-terminated-timeout=$session_terminated_timeout_ms"
[ "$stateless_proxies" = "" ]             || EXTRA_ARGS="$EXTRA_ARGS --stateless-proxies=$stateless_proxies"
[ "$max_sproutlet_depth" = "" ]           || EXTRA_ARGS="$EXTRA_ARGS --max-sproutlet-depth=$max_sproutlet_depth"
[ "$ralf_threads" = "" ]                  || EXTRA_ARGS="$EXTRA_ARGS --ralf-threads=$ralf_threads"
[ "$non_register_authentication" = "" ]   || EXTRA_ARGS="$EXTRA_ARGS --non-register-authentication=$non_register_authentication"
[ "$nonce_count_supported" != Y ]         || EXTRA_ARGS="$EXTRA_ARGS --nonce-count-supported"
[ "$listen_port" = "" ]                   || EXTRA_ARGS="$EXTRA_ARGS --listen-port=$listen_port"
[ "$blacklisted_scscf_uris" = "" ]        || EXTRA_ARGS="$EXTRA_ARGS --blacklisted-scscfs=$blacklisted_scscf_uris"

for script in "/usr/share/clearwater/$NAME/plugin_conf.d/"*.plugin_conf; do
  if [ -x "$script" ]; then
    # Include plugin configuration scripts
    EXTRA_ARGS="$EXTRA_ARGS $("$script")"
  fi
done

# TODO: needs root
#/usr/share/clearwater/bin/run-in-signaling-namespace \

"/usr/share/clearwater/bin/$NAME" \
--domain="$home_domain" \
--localhost="$local_ip" \
--realm="$home_domain" \
"$local_site_name_arg" \
--registration-stores="$sprout_registration_store" \
"$impi_store_arg" \
--hss="$hs_hostname" \
--sprout-hostname="$sprout_hostname" \
--scscf-node-uri="$scscf_node_uri" \
"$chronos_hostname_arg" \
"$sprout_chronos_callback_uri_arg" \
"$xdms_hostname_arg" \
"$ralf_arg" \
"$enum_server_arg" \
"$enum_suffix_arg" \
"$enum_file_arg" \
"$default_tel_uri_translation_arg" \
--sas="$sas_server,$NAME@$public_hostname" \
--dns-server="$signaling_dns_server" \
--worker-threads="$num_worker_threads" \
--http-threads="$num_http_threads" \
--record-routing-model="$sprout_rr_level" \
--default-session-expires="$default_session_expires" \
"$max_session_expires_arg" \
"$target_latency_us_arg" \
"$cass_target_latency_us_arg" \
"$max_tokens_arg" \
"$init_token_rate_arg" \
"$min_token_rate_arg" \
"$max_token_rate_arg" \
"$authentication_arg" \
"$user_phone_arg" \
"$sas_signaling_if_arg" \
"$disable_tcp_switch_arg" \
"$apply_fallback_ifcs_arg" \
"$reject_if_no_matching_ifcs_arg" \
"$dummy_app_server_arg" \
"$http_acr_logging_arg" \
"$global_only_lookups_arg" \
"$override_npdi_arg" \
"$exception_max_ttl_arg" \
"$force_3pr_body_arg" \
"$enable_orig_sip_to_tel_coerce_arg" \
"$request_on_queue_timeout_arg" \
--http-address="$local_ip" \
--http-port=9888 \
--analytics="$log_directory" \
--log-file="$log_directory" \
--log-level="$log_level" \
--alias="$public_ip,$public_hostname,$alias_list" \
--homestead-timeout="$sprout_homestead_timeout_ms" \
$EXTRA_ARGS \
--pidfile="$PIDFILE" &

# Note: we will use "&" instead of "--daemon" here because systemd expects a fork

# Wait for PID file to be written so that systemd doesn't emit the (harmless) warning:
# "Supervising process which is not our child"
sleep 2
