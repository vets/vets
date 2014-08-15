#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3, sys, os

# This script is to migrate from the original database table schema to the new one
# (Not necessary except for the original author's deployment or maybe if you grabbed a very early git commit)
def update_database(dbfile):
  conn = sqlite3.connect(dbfile)
  conn.row_factory = sqlite3.Row
  with conn:
    c = conn.cursor()
    # remove email and phone from volunteers, change datetime columns to timestamp to make python happier
    c.execute('ALTER TABLE volunteers RENAME TO volunteers_old')
    c.execute('CREATE TABLE "volunteers" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "name" VARCHAR(255), "orientation" TIMESTAMP, "status" VARCHAR(255), "created_at" TIMESTAMP, "updated_at" TIMESTAMP)')
    c.execute('SELECT id, name, orientation, status, created_at, updated_at FROM volunteers_old')
    volunteers = c.fetchall()
    for row in volunteers:
      c.execute('INSERT INTO volunteers (id, name, orientation, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)', (row['id'], row['name'], row['orientation'], row['status'], row['created_at'], row['updated_at']) )
    c.execute('DROP TABLE volunteers_old')
    # rename categories to activities, add status, change datetime columns to timestamp to make python happier
    c.execute('CREATE TABLE "activities" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "name" VARCHAR(255), "status" VARCHAR(255), "created_at" TIMESTAMP, "updated_at" TIMESTAMP)')
    c.execute('SELECT id, name, created_at, updated_at FROM categories')
    categories = c.fetchall()
    for row in categories:
      c.execute('INSERT INTO activities (id, name, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)', (row['id'], row['name'], 'active', row['created_at'], row['updated_at']) )
    c.execute('DROP TABLE categories')
    # change datetime columns in hours to timestamp to make python happier
    c.execute('ALTER TABLE hours RENAME TO hours_old')
    c.execute('CREATE TABLE "hours" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "volunteer_id" INTEGER, "start" TIMESTAMP, "end" TIMESTAMP, "activity_id" INTEGER, "created_at" TIMESTAMP, "updated_at" TIMESTAMP)')
    c.execute('SELECT id, volunteer_id, start, end, category_id, created_at, updated_at FROM hours_old')
    hours = c.fetchall()
    for row in hours:
      c.execute('INSERT INTO hours (id, volunteer_id, start, end, activity_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)', (row['id'], row['volunteer_id'], row['start'], row['end'], row['category_id'], row['created_at'], row['updated_at']) )
    c.execute('DROP TABLE hours_old')
    # clean up database a bit
    c.execute('VACUUM')

# Parse command line arguments
if len(sys.argv) == 2:
  if os.path.isfile(sys.argv[1]) == True:
    update_database(sys.argv[1])
  else:
    print("File {} not found)".format(sys.argv[1]))
else:
  print("Usage {} [dbfile]".format(sys.argv[0]))
