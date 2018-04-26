#
# RPM spec scriptlet utility functions
#
# For use by %%post and %%preun scriptlets in Clearwater components.
#
# (Note the required use of double %% in order to escape them in the RPM spec!)
#

#set -x

CLEARWATER_HOME=/usr/share/clearwater
MONIT_CONTROL_FILES=/etc/monit/conf.d
SECURITY_LIMITS=/etc/security/limits.conf

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

  if [ "$ACTION" != enable ] && [ "$ACTION" != disable ] && ! has_service "$NAME"; then
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

has_user ()
{
  getent passwd "$1" > /dev/null
}

has_content ()
{
  test "$(find "$1" -mindepth 1 -maxdepth 1 2> /dev/null)"
}

cw_config ()
{
  if [ -x /etc/clearwater/config ]; then
    . /etc/clearwater/config
  fi
}

cw_add_security_limits ()
{
  # TODO: can't we use /etc/security/limits.d?
  local NAME=$1

  {
    echo "#+$NAME"
    cat "/etc/security/limits.conf.$NAME"
    echo "#-$NAME"
  } >> "$SECURITY_LIMITS"
}

cw_remove_security_limits ()
{
  local NAME=$1

  local TMP_FILE=$(mktemp)

  awk '/^#\+'$NAME'$/,/^#-'$NAME'$/ {next} {print}' "$SECURITY_LIMITS" > "$TMP_FILE"
  mv "$TMP_FILE" "$SECURITY_LIMITS"
}

cw_create_user ()
{
  local NAME=$1

  local HOME_DIR="$CLEARWATER_HOME/$NAME"

  if ! has_user "$NAME"; then
    useradd --system --no-create-home --home-dir "$HOME_DIR" --shell /bin/false "$NAME"
  fi
}

cw_remove_user ()
{
  local NAME=$1

  if has_user "$NAME"; then
    userdel "$NAME"
  fi
}

cw_create_log_dir ()
{
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

cw_remove_log_dir ()
{
  local NAME=$1

  local LOG_DIR="/var/log/$NAME/"

  rm --recursive --force "$LOG_DIR"
}

cw_install_monit_control ()
{
  mkdir --parents "$MONIT_CONTROL_FILES/"
  install --mode=0644 "$1" "$MONIT_CONTROL_FILES/"
  service_action clearwater-monit reload
}

cw_update ()
{
  # Plugins
  service_action clearwater-cluster-manager restart
  service_action clearwater-config-manager restart
  service_action clearwater-queue-manager restart

  # Other possible changes
  service_action clearwater-secure-connections reload
  service_action nginx reload
}

cw_activate ()
{
  local NAME=$1

  local MONIT_CONTROL="$CLEARWATER_HOME/conf/$NAME.monit"
  local TEMPLATES="$CLEARWATER_HOME/$NAME/templates"
  local MONIT_SCRIPT="$CLEARWATER_HOME/scripts/$NAME.monit"

  # monit support (optional) can be in three (!) different places
  if [ -f "$MONIT_CONTROL" ]; then
    cw_install_monit_control "$MONIT_CONTROL"
  fi
  if [ -d "$TEMPLATES" ]; then
    for F in "$TEMPLATES"/*.monit; do
      if [ -f "$F" ]; then
        cw_install_monit_control "$F"
      fi
    done
  fi
  if [ -x "$MONIT_SCRIPT" ]; then
    mkdir --parents "$MONIT_CONTROL_FILES/"
    "$MONIT_SCRIPT"
    # It is expected that the script create a monit control file and reload monit
  fi
  
  # Run our infrastructure scripts
  service_action clearwater-infrastructure restart

  cw_update

  service_action "$NAME" enable
  service_action "$NAME" start
}

cw_deactivate ()
{
  local NAME=$1

  local TEMPLATES="$CLEARWATER_HOME/$NAME/templates"

  # monit support (optional)
  rm --force "$MONIT_CONTROL_FILES/$NAME.monit"
  if [ -d "$TEMPLATES" ]; then
    for F in "$TEMPLATES"/*.monit; do
      if [ -f "$F" ]; then
        rm "$F"
        service_action clearwater-monit reload
      fi
    done
  fi

  # Plugins
  rm --force "$CLEARWATER_HOME/clearwater-cluster-manager/plugins/$NAME"*
  rm --force "$CLEARWATER_HOME/clearwater-config-manager/plugins/$NAME"*
  rm --force "$CLEARWATER_HOME/clearwater-queue-manager/plugins/$NAME"*

  cw_update

  service_action "$NAME" stop
}

# TODO: Why does the original Clearwater packaging create the virtualenv during the %%post
# scriptlet? It seems that this should all have been done during %%install and packaged into the
# RPM. For now, we'll keep this odd solution for consistency. 

# If you use this in %%post you want to set "Requires: python-virtualenv" and also "AutoReq: no" so
# that rpmbuild won't automatically add an un-fulfillable dependency for our env/bin/python
cw_create_virtualenv ()
{
  local NAME=$1
  local PACKAGE_NAME=${2:-$NAME}

  local HOME_DIR="$CLEARWATER_HOME/$NAME"
  local ENV_DIR="$HOME_DIR/env"
  local PIP="$ENV_DIR/bin/pip"
  local WHEELHOUSE="$HOME_DIR/.wheelhouse"

  #virtualenv --no-pip --no-wheel "$ENV_DIR/"
  #"$EASY_INSTALL" "$WHEELHOUSE/wheel-"*.whl
  #"$EASY_INSTALL" "$WHEELHOUSE/pip-"*.whl

  # The virtualenv packaged with CentOS is very, very old. Its setuptools doesn't even support
  # wheels, so we have a chicken-and-egg problem with installing our included wheel and pip wheels.
  # For now, let's upgrade pip from the downloaded tarball.
  virtualenv "$ENV_DIR/"
  
  "$PIP" install --upgrade pip

  cw_add_to_virtualenv "$NAME" "$NAME" "$PACKAGE_NAME"
  chown --recursive "$NAME" "$ENV_DIR"
}

cw_add_to_virtualenv ()
{
  local ENV_NAME=$1
  local NAME=$2

  local PACKAGE_NAME=$(echo "${3:-$NAME}" | tr - _)
  local ENV_HOME_DIR="$CLEARWATER_HOME/$ENV_NAME"
  local ENV_WHEELHOUSE="$ENV_HOME_DIR/.wheelhouse"
  local ENV_DIR="$ENV_HOME_DIR/env"
  local PIP="$ENV_DIR/bin/pip"
  local HOME_DIR="$CLEARWATER_HOME/$NAME"
  local WHEELHOUSE="$HOME_DIR/.wheelhouse"

  "$PIP" install "$PACKAGE_NAME" --no-index --find-links="$ENV_WHEELHOUSE/" --find-links="$WHEELHOUSE/" \
    |& grep --invert-match 'Requirement already satisfied'
}

cw_remove_virtualenv ()
{
  local NAME=$1

  local HOME_DIR="$CLEARWATER_HOME/$NAME"
  local ENV_DIR="$HOME_DIR/env"

  rm --recursive --force "$ENV_DIR/"
}
