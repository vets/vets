#!/bin/sh

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 DBFILE" >&2
  exit 1
fi

if [ -e "$1" ]; then
  echo "$1 already exists" >&2
  exit 1
fi

cat create_tables.sql | sqlite3 $1

