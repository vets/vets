#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VETS is a Volunteer Effort Tracking System

Homepage and documentation: http://github.com/ceeekay/vets/

Copyright (c) 2014, Kevin Worth
License: MIT (see LICENSE for details)
"""
__author__  = 'Kevin Worth'
__version__ = '0.01-dev'
__license__ = 'MIT'

import os, re, sqlite3, datetime
from vendor.bottle import route, run, template, get, post, request, error, install, static_file, response

#Globals to avoid repeating myself
#db_file="db/production.sqlite3"
db_file="db/test.sqlite3"
nav = ['Volunteers', 'Hours']
message = ''

# Default columns besides internal created_at and updated_at ones
volunteer_columns = 'id, name, phone, email, orientation, status'
volunteer_column_list = [x.strip().replace('\"','') for x in volunteer_columns.split(',')]

#Cheesy way to hide admin controls (edit/delete) most of the time
global admin
admin = False

@route('/')
@route('/volunteers')
def list_volunteers(message=''):
    title = 'Volunteers'
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT %s FROM volunteers WHERE status LIKE ? ORDER BY name" % (volunteer_columns), ("active",))
    result = c.fetchall()
    c.close()
    conn.close()
    return template('_list', node='volunteers', title=title, nav=nav, message=message,
                    rows=result, cols=volunteer_column_list, admin=admin)

@route('/volunteers/new')
def new_volunteer_form():
    title = 'New Volunteer'
    return template('_edit', node='volunteers', title=title, nav=nav, message=message, cols=volunteer_column_list)

@route('/volunteers/new', method='POST')
def new_volunteer_submit():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('INSERT INTO volunteers ("name", "phone", "email", "orientation", "status", "created_at", "updated_at")\
      values (?, ?, ?, ?, ?, ?, ?)',
        (
         request.forms.get("name"),
         request.forms.get("phone"),
         request.forms.get("email"),
         request.forms.get("orientation"),
         request.forms.get("status"),
         datetime.datetime.now(),
         datetime.datetime.now()
        )
      )
    new_id = c.lastrowid
    conn.commit()
    c.close()
    conn.close()
    return list_volunteers(message="Added successfully")

@route('/volunteers/<id>')
def show_volunteer(id):
    title = 'Show Volunteer'
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT %s FROM volunteers WHERE id LIKE ?" % (volunteer_columns), (id,))
    result = c.fetchone()
    c.close()
    conn.close()
    return template('_show', node='volunteers', title=title, nav=nav, message=message, id=id, row=result, 
                    cols=volunteer_column_list, admin=admin)

@route('/volunteers/<id>/edit')
def edit_volunteer_form(id):
    title = 'Edit Volunteer'
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT %s FROM volunteers WHERE id LIKE ?" % (volunteer_columns), (id,))
    result = c.fetchone()
    c.close()
    conn.close()
    return template('_edit', node='volunteers', title=title, nav=nav, message=message, id=id,
                    cols=volunteer_column_list, values=result)

@route('/volunteers/<id>/edit', method='POST')
def edit_volunteer_submit(id):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('UPDATE volunteers SET "name" = ?, "phone" = ?, "email" = ?, "orientation" = ?, "status" = ?, "updated_at" = ?\
      where id LIKE ?',
        (
         request.forms.get("name"),
         request.forms.get("phone"),
         request.forms.get("email"),
         request.forms.get("orientation"),
         request.forms.get("status"),
         datetime.datetime.now(),
         id
        )
      )
    conn.commit()
    c.close()
    conn.close()
    return list_volunteers(message="Updated successfully")

@route('/volunteers/<id>/delete')
def delete_volunteer_confirm(id):
    title = 'Delete Volunteer'
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT %s FROM volunteers WHERE id LIKE ?" % (volunteer_columns), (id,))
    result = c.fetchone()
    c.close()
    conn.close()
    return template('_show', node='volunteers', title=title, nav=nav, message=message, id=id,
                    row=result, cols=volunteer_column_list, admin=admin, delete=True)

@route('/volunteers/<id>/delete', method='POST')
def delete_volunteer_submit(id):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("DELETE FROM volunteers WHERE id LIKE ?", (id,))
    conn.commit()
    c.close()
    conn.close()
    return list_volunteers(message="Deleted successfully")

@route('/hours')
def hours_list():
    return list_volunteers(message="Hours are still a TODO!")

@route('/admin')
def admin_on():
    global admin
    admin = True
    return list_volunteers(message="Admin mode enabled")

@route('/no_admin')
def admin_off():
    global admin
    admin = False
    return list_volunteers(message="Admin mode disabled")

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')

# TODO find/make a logo
#@route('/favicon.ico')
#def send_favicon():
#    return static_file('favicon.png', root='static')

# Go, go, go!
# run(host="", port=8888, reloader=True, debug=True)
run(host="", port=8080, reloader=True, debug=True)

