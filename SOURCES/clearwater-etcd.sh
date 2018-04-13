#!/bin/bash
set -e

# See: debian/clearwater-etcd.init.d

NAME=clearwater-etcd

log_level=2
etcd_version=3.1.7

. /etc/clearwater/config

listen_ip=${management_local_ip:-$local_ip}
advertisement_ip=${management_local_ip:-$local_ip}
DATA_DIR="/var/lib/$NAME"
JOINED_CLUSTER_SUCCESSFULLY="$DATA_DIR/clustered_successfully"
HEALTHY_CLUSTER_VIEW="$DATA_DIR/healthy_etcd_members"
ETCD_NAME=${advertisement_ip//./-}
LOG_FILE="/var/log/$NAME/$NAME-systemd.log"


log_info () {
  echo $(date +'%Y-%m-%d %H:%M:%S.%N') "$@" >> $LOG_FILE
}


log_debug () {
  echo "$@"
  log_debug "$@"
}


# Wrapper that runs etcdctl but also logs the following to the log file:
# - The etcdctl command being run
# - stdout and stderr from the command
# - The status code from the command
etcdctl_wrapper () {
  log_debug "Running etcdctl $@"

  # Run the etcdctl command and capture stdout and stderr to the log file.
  #
  # The redirections in this command are a bit insane:
  # a)  Make file descriptor 7 a copy of the original stdout
  # b)  Redirect stdout to the original stderr.
  # c)  Redirect stderr to a temporary FD that is passed to the stdin of a tee
  #     subcommand. This writes all its input to the log file and to the stdout
  #     inherited from its parent. But the parent stdout is currently pointing
  #     at the original stderr.
  # d)  Restore stdout to the original stdout (currently pointed to by FD 7).
  # e)  Redirect stdout to another tee command. This command's stdout is the
  #     original stdout.
  # f)  We're done with FD 7, so close it.
  #
  # The end result of all this is that the stdout and stderr of the etcdctl
  # command go to same place as if we hadn't done any of this, but they are also
  # captured to the log file.
  #
  # We also save off the status code from etcdctl so it can be logged and
  # returned. Despite all our shenanigans we've only run one command in this
  # shell, so $? does indeed contain the exit code from etcdctl.
  "/usr/share/clearwater/$NAME/$etcd_version/etcdctl" "$@" \
    7>&1 \
    1>&2 \
    2> >(tee -a "$LOG_FILE") \
    1>&7 \
    1> >(tee -a "$LOG_FILE") \
    7>&-
  retcode=$?

  log_debug "etcdctl returned $retcode"

  return $retcode
}


generate_initial_cluster () {
  # We are provided with a comma or space separated list of IP
  # addresses. We need to produce a list of comma separated
  # entries, where each entry should look like <name>=<peer url>.
  # Replace commas with whitespace, then split on whitespace (to
  # cope with etcd_cluster values that have spaces)
  # We generate names by just replacing dots with dashes.
  ETCD_INITIAL_CLUSTER=
  for server in ${1//,/ }; do
      server_name=${server%:*}
      server_name=${server_name//./-}
      ETCD_INITIAL_CLUSTER="${server_name}=http://$server:2380,$ETCD_INITIAL_CLUSTER"
  done
}


create_cluster () {
  log_info "Creating new cluster..."

  # Build the initial cluster view string based on the IP addresses in
  # $etcd_cluster.
  generate_initial_cluster "$etcd_cluster"

  CLUSTER_ARGS="--initial-cluster \"$ETCD_INITIAL_CLUSTER\"
                --initial-cluster-state new"
}


join_cluster_as_proxy () {
  log_info "Joining cluster as proxy..."

  # We can either be supplied with a complete proxy setup string
  # in $etcd_proxy, or a list of IP addresses, like etcd_cluster
  # Disambiguate the two based on if it has an "=" sign it.
  if [[ $etcd_proxy == *"="* ]]; then
      ETCD_INITIAL_CLUSTER="$etcd_proxy"
  else
      # Build the initial cluster view string based on the IP addresses in
      # $etcd_proxy.
      generate_initial_cluster "$etcd_proxy"
  fi

  CLUSTER_ARGS="--initial-cluster \"$ETCD_INITIAL_CLUSTER\" --proxy on"
}


setup_etcdctl_peers () {
  # If we were in a working cluster before, we will have saved off an up to
  # date view of the cluster. We want to override etcd_cluster or
  # etcd_proxy with this, so that functions later in this script use the
  # correct cluster value.
  if [ -f "$HEALTHY_CLUSTER_VIEW" ]; then
    # We want to stip anything up to and including the first = character
    # so we can select etcd_cluster or etcd_proxy appropriately
    healthy_cluster=$(sed -e 's/.*=//' < "$HEALTHY_CLUSTER_VIEW")

    # We also want to ensure that the file was not just empty, so verify
    # that stripping white space still leaves something
    if [ -z "${healthy_cluster// /}" ]; then
      log_debug "healthy cluster view was empty, using config values instead"
    else
      # Set etcd_cluster or etcd_proxy to the values we found in the
      # healthy cluster view, based on what is provided in config
      if [ -n "$etcd_cluster" ]; then
        etcd_cluster="$healthy_cluster"
      elif [ -n "$etcd_proxy" ]; then
        etcd_proxy="$healthy_cluster"
      fi
    fi
  fi

  # Build the client list based on $etcd_cluster. Each entry is simply
  # <IP>:<port>, using the client port. Replace commas with whitespace,
  # then split on whitespace (to cope with etcd_cluster values that have spaces)
  export ETCDCTL_PEERS=
  servers=""
  if [ -n "$etcd_cluster" ]; then
    servers=$etcd_cluster
  elif [ -n "$etcd_proxy" ]; then
    servers=$etcd_proxy
  fi

  for server in ${servers//,/ }; do
    if [ "$server" != "$advertisement_ip" ]; then
      ETCDCTL_PEERS="$server:4000,$ETCDCTL_PEERS"
    fi
  done

  log_debug "Configured ETCDCTL_PEERS: $ETCDCTL_PEERS"
}


join_cluster () {
  # Joining existing cluster
  log_info "Joining existing cluster..."

  # If this fails, then hold off trying again for a time. This stops us
  # overwhelming the etcd elections on a large scale-up.
  sleep $[$RANDOM%30]

  # We need a temp file to deal with the environment variables.
  TEMP_FILE=$(mktemp)

  setup_etcdctl_peers

  # Check to make sure the cluster we want to join is healthy.
  # If it's not, don't even try joining (it won't work, and may
  # cause problems with the cluster)
  log_debug "Check cluster is healthy"
  etcdctl_wrapper cluster-health 2>&1 | grep "cluster is healthy"
  if [ "$?" -ne 0 ]; then
    log_info "Not joining an unhealthy cluster"
    exit 2
  fi

  # Tell the cluster we're joining
  log_debug "Tell the cluster we're joining"
  etcdctl_wrapper member add "$ETCD_NAME" "http://$advertisement_ip:2380"
  if [ "$?" != 0 ]; then
    local_member_id=$(etcdctl_wrapper member list | grep -F -w "http://$advertisement_ip:2380" | grep -o -E "^[^:]*" | grep -o "^[^[]\+")
    etcdctl_wrapper member remove "$local_member_id"
    rm -rf "$DATA_DIR/$advertisement_ip"
    log_info "Failed to add local node $advertisement_ip to the etcd cluster"
    logger -p daemon.error -t $NAME Failed to add the local node \($advertisement_ip\) to the etcd cluster
    exit 2
  fi

  ETCD_INITIAL_CLUSTER=$(/usr/share/clearwater/bin/get_etcd_initial_cluster.py $advertisement_ip $etcd_cluster)

  CLUSTER_ARGS="--initial-cluster \"$ETCD_INITIAL_CLUSTER\"
                --initial-cluster-state existing"

  # Tidy up
  rm "$TEMP_FILE"
}

#
# Function to join/create an etcd cluster based on the `etcd_cluster` variable
#
# Sets the CLUSTER_ARGS variable to an appropriate value to use as arguments to
# etcd.
#
join_or_create_cluster()
{
  # We only want to create the cluster if we are both a founding member,
  # and we have never successfully clustered before. Otherwise, we join
  if [[ ! -f "$JOINED_CLUSTER_SUCCESSFULLY" && ${etcd_cluster//,/ } =~ (^| )$advertisement_ip( |$) ]]; then
    create_cluster
  else
    join_cluster
  fi
}


verify_etcd_health_after_startup () {
  # We could be in a bad state at this point - parse the etcd logs for
  # known error conditions. We do this from the logs as they're the most
  # reliable way of detecting that something is wrong.

  # We could have a data directory already, but not actually be a member of
  # the etcd cluster. Remove the data directory.
  log_debug "Check we're actually a member of the cluster"
  tail -10 "/var/log/$NAME/$NAME.log" | grep -q "etcdserver: the member has been permanently removed from the cluster"
  if [ "$?" == 0 ]; then
    log_info "Etcd is in an inconsistent state - removing the data directory"
    logger -p daemon.error -t $NAME Etcd is in an inconsistent state - removing the data directory
    rm -rf "$DATA_DIR/$advertisement_ip"
    exit 3
  fi

  # Wait for etcd to come up. Note - all this tests is that clearwater-etcd
  # is listening on 4000 - it doesn't confirm that etcd is running fully
  log_debug "Wait for etcd to startup"

  start_time=$(date +%s)
  while true; do
    if nc -z "$listen_ip" 4000; then
      touch "$JOINED_CLUSTER_SUCCESSFULLY"
      break
    else
      current_time=$(date +%s)
      let "delta_time=$current_time - $start_time"
      if [ "$delta_time" -gt 60 ]; then
        log_info "Etcd failed to start"
        logger -p daemon.error -t $NAME Etcd failed to start
        exit 2
      fi
      sleep 1
    fi
  done

  log_debug "etcd started successfully"
}


verify_etcd_health_before_startup () {
  # If we're already in the member list but are 'unstarted', remove our data dir, which
  # contains stale data from a previous unsuccessful startup attempt. This copes with a race
  # condition where member add succeeds but etcd doesn't then come up.
  #
  # The output of member list looks like:
  # <id>[unstarted]: name=xx-xx-xx-xx peerURLs=http://xx.xx.xx.xx:2380 clientURLs=http://xx.xx.xx.xx:4000
  # The [unstarted] is only present while the member hasn't fully joined the etcd cluster
  setup_etcdctl_peers

  log_debug "Check for previous failed startup attempt"
  member_list=$(etcdctl_wrapper member list)
  local_member_id=$(echo "$member_list" | grep -F -w "http://$local_ip:2380" | grep -o -E "^[^:]*" | grep -o "^[^[]\+")
  unstarted_member_id=$(echo "$member_list" | grep -F -w "http://$local_ip:2380" | grep "unstarted")
  if [ "$unstarted_member_id" != '' ]; then
    log_debug "etcd failed to start successfully on a previous attempt - removing the data directory"
    logger -p daemon.error -t $NAME Etcd failed to start successfully on a previous attempt - removing the data directory
    etcdctl_wrapper member remove "$local_member_id"
    rm -rf "$DATA_DIR/$advertisement_ip"
  fi

  if [ -e "$DATA_DIR/$advertisement_ip" ]; then
    # Check we can read our write-ahead log and snapshot files. If not, our
    # data directory is irrecoverably corrupt (perhaps because we ran out
    # of disk space and the files were half-written), so we should clean it
    # out and rejoin the cluster from scratch.
    log_debug "Check we can read files in the data directory"
    timeout 5 "/usr/share/clearwater/$NAME/$etcd_version/etcd-dump-logs" --data-dir "$DATA_DIR/$advertisement_ip" > /dev/null 2>&1
    rc=$?

    if [ "$rc" != 0 ]; then
      log_debug "The etcd data is corrupted - removing the data directory"
      logger -p daemon.error -t $NAME The etcd data is corrupted - removing the data directory
      etcdctl_wrapper member remove "$local_member_id"
      rm -rf "$DATA_DIR/$advertisement_ip"
    fi
  fi
}


verify_etcd_health_before_startup

if [ -n "$etcd_cluster" ] && [ -n "$etcd_proxy" ]; then
  log_info "Cannot specify both etcd_cluster and etcd_proxy"
  exit 2
elif [ -n "$etcd_cluster" ]; then
  # Join or create the etcd cluster as a full member
  if [ -d "/var/lib/$NAME/$advertisement_ip" ]; then
    # We'll start normally using the data we saved off on our last boot
    log_info "Rejoining cluster..."
  else
    join_or_create_cluster
  fi

  # Add common clustering parameters
  CLUSTER_ARGS="$CLUSTER_ARGS
                --initial-advertise-peer-urls \"http://$advertisement_ip:2380\"
                --listen-peer-urls \"http://$listen_ip:2380\""
elif [ -n "$etcd_proxy" ]; then
  # Run etcd as a proxy talking to the cluster
  join_cluster_as_proxy
else
  log_info "Must specify either etcd_cluster or etcd_proxy"
  exit 2
fi

"/usr/share/clearwater/$NAME/$etcd_version/etcd" \
  --listen-client-urls http://0.0.0.0:4000 \
  --advertise-client-urls "http://$advertisement_ip:4000" \
  --data-dir "$DATA_DIR/$advertisement_ip" \
  --name "$ETCD_NAME" \
  --debug \
  $CLUSTER_ARGS

# TODO: won't be called
verify_etcd_health_after_startup
