#
# RPM spec scriptlet utility functions
#
# For use by %%post and %%preun scriptlets in Clearwater components.
#

#set -x

CLEARWATER_HOME=/usr/share/clearwater
MONIT_CONTROL_FILES=/etc/monit/conf.d
SECURITY_LIMITS=/etc/security/limits.conf

has-content ()
{
 if [ -d "$1" ]; then
   find "$1" -mindepth 1 -print -quit | grep -q .
   return $?
 fi
 return 1
}

service-action ()
{
  local NAME=$1
  local ACTION=$2
  local SERVICE="$NAME.service"

  if [ -f /usr/bin/monit ]; then
    if [ "$ACTION" = start ]; then
      # monit will restart it
      ACTION=stop
    elif [ "$ACTION" = restart ]; then
      # monit will restart it
      ACTION=stop
    fi
  fi

  if [ "$ACTION" = stop ]; then
    if systemctl --quiet is-active "$SERVICE"; then # no need to stop if already stopped
      systemctl stop "$SERVICE" || /bin/true
    fi
  else 
    systemctl "$ACTION" "$SERVICE" || /bin/true
  fi
}

cw-config ()
{
  if [ -f /etc/clearwater/config ]; then
    . /etc/clearwater/config
  fi
}

cw-add-security-limits ()
{
  # TODO: can't we use /etc/security/limits.d?
  local NAME=$1
  {
    echo "#+$NAME"
    cat "/etc/security/limits.conf.$NAME"
    echo "#-$NAME"
  } >> "$SECURITY_LIMITS"
}

cw-remove-security-limits ()
{
  local NAME=$1
  local TMP_FILE=$(mktemp)
  awk '/^#\+'$NAME'$/,/^#-'$NAME'$/ {next} {print}' "$SECURITY_LIMITS" > "$TMP_FILE"
  mv "$TMP_FILE" "$SECURITY_LIMITS"
}

cw-create-user ()
{
  local NAME=$1
  local HOME_DIR="$CLEARWATER_HOME/$NAME"
  if ! getent passwd "$NAME" &> /dev/null; then
    useradd --system --no-create-home --home-dir "$HOME_DIR" --shell /bin/false "$NAME"
  fi
}

cw-remove-user ()
{
  local NAME=$1
  if getent passwd "$NAME" &> /dev/null; then
    userdel "$NAME"
  fi
}

cw-create-log-dir ()
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

cw-remove-log-dir ()
{
  local NAME=$1
  local LOG_DIR="/var/log/$NAME/"
  rm --recursive --force "$LOG_DIR"
}

cw-start ()
{
  local NAME=$1
  local MONIT="/usr/share/clearwater/conf/$NAME.monit"
  local TEMPLATES="/usr/share/clearwater/$NAME/templates"

  # monit support (optional)
  if [ -f "$MONIT" ]; then
    mkdir --parents "$MONIT_CONTROL_FILES/"
    install --mode=0644 "$MONIT" "$MONIT_CONTROL_FILES/"
  fi
  if has-content "$TEMPLATES/"; then
    cp "$TEMPLATES/"*.monit "$MONIT_CONTROL_FILES/"
  fi

  service-action clearwater-infrastructure restart # run our restart scripts
  service-action clearwater-secure-connections reload
  service-action clearwater-monit reload # read our new monit control files
  service-action clearwater-cluster-manager start
  service-action "$NAME" enable
  service-action "$NAME" start
}

cw-stop ()
{
  local NAME=$1
  local TEMPLATES="/usr/share/clearwater/$NAME/templates"

  # monit support (optional)
  rm --force "$MONIT_CONTROL_FILES/$NAME.monit"
  if [ -d "$TEMPLATES" ]; then
    for F in "$TEMPLATES"/*.monit; do
      rm --force "$MONIT_CONTROL_FILES/$(basename "$F")"
    done
  fi

  rm --force "/usr/share/clearwater/clearwater-cluster-manager/plugins/$NAME"*

  service-action nginx reload
  service-action clearwater-secure-connections reload
  service-action clearwater-monit reload # forget our monit control files
  service-action clearwater-cluster-manager stop # monit will restart it if it's installed
  service-action "$NAME" stop # monit will *not* restart it
}

# TODO: Why does the original Clearwater packaging create the virtualenv during the %%post
# scriptlet? It seems that this should all have been done during %%install and packaged into the
# RPM. For now, we'll keep this odd solution for consistency. 

# If you use this in %%post you want to set "Requires: python-virtualenv" and also "AutoReq: no" so
# that rpmbuild won't automatically add an un-fulfillable dependency for our env/bin/python
cw-create-virtualenv ()
{
  local NAME=$1
  local PACKAGE_NAME=${2:-$NAME}
  local HOME_DIR="$CLEARWATER_HOME/$NAME"
  local ENV_DIR="$HOME_DIR/env"
  local EASY_INSTALL="$ENV_DIR/bin/easy_install"
  local PIP="$ENV_DIR/bin/pip"
  local WHEELHOUSE="$HOME_DIR/.wheelhouse"
  virtualenv --no-pip --no-wheel "$ENV_DIR/"
  "$EASY_INSTALL" "$WHEELHOUSE/pip-"*.whl
  "$PIP" install wheel --no-index --find-links="$WHEELHOUSE/" \
    |& grep --invert-match 'Requirement already satisfied'
  cw-add-to-virtualenv "$NAME" "$NAME" "$PACKAGE_NAME"
}

cw-add-to-virtualenv ()
{
  local ENV_NAME=$1
  local NAME=$2
  local PACKAGE_NAME=${3:-$NAME}
  local ENV_HOME_DIR="$CLEARWATER_HOME/$ENV_NAME"
  local ENV_WHEELHOUSE="$ENV_HOME_DIR/.wheelhouse"
  local ENV_DIR="$ENV_HOME_DIR/env"
  local PIP="$ENV_DIR/bin/pip"
  local HOME_DIR="$CLEARWATER_HOME/$NAME"
  local WHEELHOUSE="$HOME_DIR/.wheelhouse"
  "$PIP" install "$PACKAGE_NAME" --no-index --find-links="$ENV_WHEELHOUSE/" --find-links="$WHEELHOUSE/" \
    |& grep --invert-match 'Requirement already satisfied'
}

cw-remove-virtualenv ()
{
  local NAME=$1
  local HOME_DIR="$CLEARWATER_HOME/$NAME"
  local ENV_DIR="$HOME_DIR/env"
  rm --recursive --force "$ENV_DIR/"
}
