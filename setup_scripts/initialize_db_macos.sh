#! /usr/bin/env bash
set -e
DB_NAME='minidetector'
USER='detector'

[ -d /usr/local/var/postgres ] || initdb /usr/local/var/postgres
brew services restart postgresql
sleep 5 # wait for db to finish startup
dropdb --if-exists -f $DB_NAME
dropuser --if-exists $USER
createuser --superuser $USER
createdb --owner $USER $DB_NAME
echo DONE!
