
#
# These functions are in Debian's /lib/lsb/init-functions, but are not in CentOS 7.4
# (redhat-lsb-core package).
#
# Instead of overwriting /lib/lsb/init-functions, we'll put them in /lib/init/vars.sh, which is
# doesn't exist in CentOS but is always sourced by Debian init scripts. Hack!
#

# The following are copied from Debian:

status_of_proc () {
    local pidfile daemon name status OPTIND

    pidfile=
    OPTIND=1
    while getopts p: opt ; do
        case "$opt" in
            p)  pidfile="$OPTARG";;
        esac
    done
    shift $(($OPTIND - 1))

    if [ -n "$pidfile" ]; then
        pidfile="-p $pidfile"
    fi
    daemon="$1"
    name="$2"

    status="0"
    pidofproc $pidfile $daemon >/dev/null || status="$?"
    if [ "$status" = 0 ]; then
        log_success_msg "$name is running"
        return 0
    elif [ "$status" = 4 ]; then
        log_failure_msg "could not access PID file for $name"
        return $status
    else
        log_failure_msg "$name is not running"
        return $status
    fi
}

log_use_fancy_output () {
    TPUT=/usr/bin/tput
    EXPR=/usr/bin/expr
    if  [ -t 1 ] &&
	[ "x${TERM:-}" != "x" ] &&
	[ "x${TERM:-}" != "xdumb" ] &&
	[ -x $TPUT ] && [ -x $EXPR ] &&
	$TPUT hpa 60 >/dev/null 2>&1 &&
	$TPUT setaf 1 >/dev/null 2>&1
    then
        [ -z $FANCYTTY ] && FANCYTTY=1 || true
    else
        FANCYTTY=0
    fi
    case "$FANCYTTY" in
        1|Y|yes|true)   true;;
        *)              false;;
    esac
}

log_daemon_msg_pre () {
    if log_use_fancy_output; then
        echo -n "[....] " || true
    fi
}

log_daemon_msg_post () { :; }

log_begin_msg_pre () {
    log_daemon_msg_pre "$@"
}

log_end_msg_pre () {
    if log_use_fancy_output; then
        RED=$( $TPUT setaf 1)
        GREEN=$( $TPUT setaf 2)
        YELLOW=$( $TPUT setaf 3)
        NORMAL=$( $TPUT op)

        $TPUT civis || true
        $TPUT sc && \
        $TPUT hpa 0 && \
        if [ $1 -eq 0 ]; then
            /bin/echo -ne "[${GREEN} ok ${NORMAL}" || true
        elif [ $1 -eq 255 ]; then
            /bin/echo -ne "[${YELLOW}warn${NORMAL}" || true
        else
            /bin/echo -ne "[${RED}FAIL${NORMAL}" || true
        fi && \
        $TPUT rc || true
        $TPUT cnorm || true
    fi
}

log_end_msg_post () { :; }

log_daemon_msg () {
    if [ -z "${1:-}" ]; then
        return 1
    fi
    log_daemon_msg_pre "$@"

    if [ -z "${2:-}" ]; then
        echo -n "$1:" || true
        return
    fi
    
    echo -n "$1: $2" || true
    log_daemon_msg_post "$@"
}

log_end_msg () {
    # If no arguments were passed, return
    if [ -z "${1:-}" ]; then
        return 1
    fi

    local retval
    retval=$1

    log_end_msg_pre "$@"

    # Only do the fancy stuff if we have an appropriate terminal
    # and if /usr is already mounted
    if log_use_fancy_output; then
        RED=$( $TPUT setaf 1)
        YELLOW=$( $TPUT setaf 3)
        NORMAL=$( $TPUT op)
    else
        RED=''
        YELLOW=''
        NORMAL=''
    fi

    if [ $1 -eq 0 ]; then
        echo "." || true
    elif [ $1 -eq 255 ]; then
        /bin/echo -e " ${YELLOW}(warning).${NORMAL}" || true
    else
        /bin/echo -e " ${RED}failed!${NORMAL}" || true
    fi
    log_end_msg_post "$@"
    return $retval
}