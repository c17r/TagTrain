#!/usr/bin/env bash

RUN=$PWD/run
CURRENT=$RUN/current

PIDFILE=$RUN/tagtrain.pid
LOGFILE=$RUN/logs/tagtrain.log
DATFILE=$RUN/tagtrain.db
CONFILE=$RUN/config.json

source "$CURRENT/venv/bin/activate"

tagtrain $1 --pid-file "$PIDFILE" --log-file "$LOGFILE" --db-file "$DATFILE" --config-file "$CONFILE"
