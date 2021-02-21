# bash .profile
mkdir -p /home/nfatools/data/download
export NFATOOLS_PROFILE=${NFATOOLS_PROFILE:-nfatools/form3}
chamber_read() {
    chamber read $NFATOOLS_PROFILE -q $1
}
cat ->.my.cnf <<EOF
[client]
host=$(chamber_read DB_HOST)
port=$(chamber_read DB_PORT)
user=$(chamber_read DB_USER)
password=$(chamber_read DB_PASSWORD)
database=$(chamber_read DB_DATABASE)
EOF
