CLEARWATER_HOME=/usr/share/clearwater
MONIT_CONTROL_FILES=/etc/monit/conf.d/
SECURITY_LIMITS=/etc/security/limits.conf

function service-action {
  NAME=$1
  ACTION=$2
  SERVICE="$NAME.service"
  if [ -f "/etc/init.d/$NAME" ]; then
    if [ "$ACTION" = stop ]; then
      if systemctl --quiet is-active "$SERVICE"; then
        systemctl "$ACTION" || /bin/true
      fi
    else 
      systemctl "$ACTION" "$SERVICE" || /bin/true
    fi
  fi
}

function cw-add-security-limits {
  local NAME=$1
  {
    echo "#+$NAME"
    cat "/etc/security/limits.conf.$NAME"
    echo "#-$NAME"
  } >> "$SECURITY_LIMITS"
}

function cw-remove-security-limits {
  local NAME=$1
  local TMP_FILE=$(mktemp)
  awk '/^#\+'$NAME'$/,/^#-'$NAME'$/ {next} {print}' "$SECURITY_LIMITS" > "$TMP_FILE"
  mv "$TMP_FILE" "$SECURITY_LIMITS"
}

function cw-create-user {
  local NAME=$1
  local HOME_DIR="$CLEARWATER_HOME/$NAME"
  if ! id "$NAME" > /dev/null 2>&1; then
    useradd --system --no-create-home --home-dir "$HOME_DIR" --shell /bin/false "$NAME"
  fi
}

function cw-remove-user {
  local NAME=$1
  if id "$NAME" > /dev/null 2>&1; then
    userdel "$NAME"
  fi
}

function cw-create-log-dir {
  local NAME=$1
  local GROUP=${2:-root}
  local LOG_DIR="/var/log/$NAME/"
  mkdir --parents --mode=755 "$LOG_DIR"
  chown --recursive "$NAME:$GROUP" "$LOG_DIR"
  if [ "$GROUP" != root ]; then
    chmod g+s --recursive "$LOG_DIR"
  fi
  if [ -x "$CLEARWATER_HOME/bin/clearwater-logging-update" ]; then
  	"$CLEARWATER_HOME/bin/clearwater-logging-update"
  fi
}

function cw-remove-log-dir {
  local NAME=$1
  local LOG_DIR="/var/log/$NAME/"
  rm --recursive --force "$LOG_DIR"
}

function cw-remove-run-dir {
  local NAME=$1
  local RUN_DIR="/var/run/$NAME/"
  rm --recursive --force "$RUN_DIR"
}

function cw-start {
  local NAME=$1
  local MONIT="/usr/share/clearwater/conf/$NAME.monit"
  if [ -f "$MONIT" ]; then
    mkdir --parents "$MONIT_CONTROL_FILES"
    install --mode=0644 "$MONIT" "$MONIT_CONTROL_FILES"
  fi
  service-action clearwater-infrastructure restart # run our install scripts
  service-action clearwater-secure-connections reload
  service-action clearwater-monit reload # read our new monit control files
  service-action clearwater-cluster-manager stop # monit will restart it if it's installed
  service-action "$NAME" stop # in case it's already running (an upgrade); monit will start it
}

function cw-stop {
  local NAME=$1
  rm --force "/etc/monit/conf.d/$NAME.monit"
  rm --force "/usr/share/clearwater/clearwater-cluster-manager/plugins/$NAME"*
  service-action clearwater-secure-connections reload
  service-action clearwater-monit reload # forget our monit control files
  service-action clearwater-cluster-manager stop # monit will restart it if it's installed
  service-action "$NAME" stop # monit will *not* restart it
}

function cw-create-virtualenv {
  local NAME=$1
  local HOME_DIR="$CLEARWATER_HOME/$NAME"
  local WHEELHOUSE="$HOME_DIR/wheelhouse"
  local ENV_DIR="$CLEARWATER_HOME/$NAME/env"
  local PIP="$ENV_DIR/bin/pip"
  virtualenv "$ENV_DIR/"
  "$PIP" install --upgrade pip
  #"$PIP" install "$WHEELHOUSE/pip-"*.whl
  "$PIP" install --no-index --find-links "$WHEELHOUSE/" wheel "$NAME"
}

function cw-remove-virtualenv {
  local NAME=$1
  local HOME_DIR="$CLEARWATER_HOME/$NAME"
  local ENV_DIR="$CLEARWATER_HOME/$NAME/env"
  rm --recursive --force "$ENV_DIR/"
}

