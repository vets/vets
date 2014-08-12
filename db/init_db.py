#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3, sys

volunteers_create = 'CREATE TABLE "volunteers" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "name" VARCHAR(255), "orientation" TIMESTAMP, "status" VARCHAR(255), "created_at" TIMESTAMP, "updated_at" TIMESTAMP)'
categories_create = 'CREATE TABLE "categories" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "name" VARCHAR(255), "status" VARCHAR(255), "created_at" TIMESTAMP, "updated_at" TIMESTAMP)'
hours_create = 'CREATE TABLE "hours" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "volunteer_id" INTEGER, "start" TIMESTAMP, "end" TIMESTAMP, "category_id" INTEGER, "created_at" TIMESTAMP, "updated_at" TIMESTAMP)'

def create_database(dbfile):
  conn = sqlite3.connect(dbfile)
  with conn:
    c = conn.cursor()
    c.execute(volunteers_create)
    c.execute(categories_create)
    c.execute(hours_create)  

def update_database(dbfile):
  conn = sqlite3.connect(dbfile)
  conn.row_factory = sqlite3.Row
  with conn:
    c = conn.cursor()
    # remove email and phone from volunteers, change datetime columns to timestamp to make python happier
    c.execute('ALTER TABLE volunteers RENAME TO volunteers_old')
    c.execute(volunteers_create)
    c.execute('SELECT id, name, orientation, status, created_at, updated_at FROM volunteers_old')
    volunteers = c.fetchall()
    for row in volunteers:
      c.execute('INSERT INTO volunteers (id, name, orientation, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)', (row['id'], row['name'], row['orientation'], row['status'], row['created_at'], row['updated_at']) )
    c.execute('DROP TABLE volunteers_old')
    # add status to categories, change datetime columns to timestamp to make python happier
    c.execute('ALTER TABLE categories RENAME TO categories_old')
    c.execute(categories_create)
    c.execute('SELECT id, name, created_at, updated_at FROM categories_old')
    categories = c.fetchall()
    for row in categories:
      c.execute('INSERT INTO categories (id, name, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)', (row['id'], row['name'], 'active', row['created_at'], row['updated_at']) )
    c.execute('DROP TABLE categories_old')
    # change datetime columns in hours to timestamp to make python happier
    c.execute('ALTER TABLE hours RENAME TO hours_old')
    c.execute(hours_create)
    c.execute('SELECT id, volunteer_id, start, end, category_id, created_at, updated_at FROM hours_old')
    hours = c.fetchall()
    for row in hours:
      c.execute('INSERT INTO hours (id, volunteer_id, start, end, category_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)', (row['id'], row['volunteer_id'], row['start'], row['end'], row['category_id'], row['created_at'], row['updated_at']) )
    c.execute('DROP TABLE hours_old')
    # clean up database a bit
    c.execute('VACUUM')


if len(sys.argv) == 1 or sys.argv[0] == '-h':
  print "Usage {} -c | -u  [dbfile]".format(sys.argv[0])
elif len(sys.argv) > 1 and sys.argv[1] == '-c':
  if len(sys.argv) > 2:
    create_database(sys.argv[2])
  else:
    create_database("development.sqlite3")
elif len(sys.argv) > 1 and sys.argv[1] == '-u':
  if len(sys.argv) > 2:
    update_database(sys.argv[2])
  else:
    update_database("development.sqlite3")
