function log_daemon_msg {
  echo $@
}

function log_end_msg {
  retval=$1
  if [ $retval -eq 0 ]; then
    echo '.'
  else
    echo ' failed!'
  fi
  return $retval
}
