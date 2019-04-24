#!/usr/bin/env bash

RUN=$PWD/local
CURRENT=$RUN/current

PIDFILE=$RUN/tagtrain.pid
LOGFILE=$RUN/tagtrain.log
DATFILE=$RUN/tagtrain.db
CONFILE=$RUN/config.json

pipenv run python -m src.tagtrain cli --pid-file "$PIDFILE" --log-file "$LOGFILE" --db-file "$DATFILE" --config-file "$CONFILE"