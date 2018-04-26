
has_monit ()
{
  test -x /usr/bin/monit
}

has_service ()
{
  test "$(systemctl status "$1.service" 2> /dev/null)" 
}

is_service_active ()
{
  systemctl is-active "$1.service" > /dev/null 
}

service_action ()
{
  local NAME=$1
  local ACTION=$2

  local SERVICE="$NAME.service"

  if ! has_service "$SERVICE"; then
    return
  fi
  
  if has_monit; then
    if [ "$ACTION" = start ]; then
      # It is expected that monit will start it
      return
    elif [ "$ACTION" = restart ]; then
      # It is expected that monit will restart it
      ACTION=stop
    fi
  fi

  if [ "$ACTION" = stop ]; then
    if is_service_active "$SERVICE"; then # no need to stop if already stopped
      systemctl stop "$SERVICE" || /bin/true
    fi
  else 
    systemctl "$ACTION" "$SERVICE" || /bin/true
  fi
}
