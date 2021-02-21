#!/bin/bash

# NFATOOLS-FORM3 Entrypoint
. .profile

export PATH=${HOME}/.local/bin:$PATH

chgrp selenium /home/nfatools/data/download
chmod g+rwx /home/nfatools/data/download

function shutdown {
  echo "SIGTERM: stopping form3 service"
  exit
}
trap shutdown SIGTERM
trap shutdown SIGINT

set_mysql_config

COMMAND=${NFATOOLS_COMMAND:=run}

case $COMMAND in 
  run)	
    touch nfatools.log
    (chamber exec $NFATOOLS_PROFILE -- form3 run)&
    (tail -f nfatools.log >/proc/1/fd/1)&
    sleep infinity&
    wait
  ;;
  shell)
    chamber exec $NFATOOLS_PROFILE -- bash -l
  ;;
  *)
    exec "$@"
  ;;
esac
