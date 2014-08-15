#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3, sys, os

def restore_database(backupfile):
  dbfile = "{}ite3".format(backupfile)
  with sqlite3.connect(dbfile) as conn:
    conn.isolation_level = None
    c = conn.cursor()
    with open(backupfile, 'r') as f:
      for line in f:
        c.execute(line)

# Parse command line arguments
if len(sys.argv) == 2:
  if os.path.isfile(sys.argv[1]) == True:
    restore_database(sys.argv[1])
  else:
    print("Backup file {} not found)".format(sys.argv[1]))
else:
  print("Usage {} backups/backup-DESIRED_TIMESTAMP.sql".format(sys.argv[0]))
