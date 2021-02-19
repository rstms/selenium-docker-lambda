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

case $1 in 
  run)	
    touch ./log/nfatools.log
    (tail -f ./log/nfatools.log >/proc/1/fd/1)&
    sleep infinity&
    wait
  ;;
  *)
    exec "$@"
  ;;
esac
