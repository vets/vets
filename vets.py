#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VETS is a Volunteer Effort Tracking System

Homepage and documentation: https://github.com/vets/vets/

Copyright (c) 2014, Kevin Worth
License: MIT (see LICENSE for details)
"""
__author__  = 'Kevin Worth'
__version__ = '0.02-dev'
__license__ = 'MIT'

import os, re, sqlite3, datetime
from vendor.bottle import route, run, template, get, post, request, error, install, static_file, response

#Database settings
conn = sqlite3.connect("db/test.sqlite3")
conn.row_factory = sqlite3.Row

#Globals for commonly passed stuff
nav = ['Volunteers', 'Hours']
message = ''

#Cheesy way to hide admin controls most of the time
global admin
admin = False

#Volunteer handlers

@route('/')
@route('/volunteers')
@route('/volunteers/<status:re:active|inactive>')
def list_volunteers(message='', status='active'):
    title = '%s Volunteers' % (status.title())
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, date(orientation), status FROM volunteers WHERE status = ? ORDER BY name", (status,))
      result = c.fetchall()
    return template('volunteer_list', title=title, nav=nav, message=message, rows=result, status=status)

@route('/volunteers/new')
def new_volunteer_form(message=''):
    title = 'New Volunteer'
    return template('volunteer_edit', title=title, nav=nav, message=message)

@route('/volunteers/new', method='POST')
def new_volunteer_submit():
    if request.forms.get('name') == '':
      return new_volunteer_form("Please enter a Name")
    if request.forms.get('orientation') == '':
      return new_volunteer_form("Please select an Orientation date")
    with conn:
      c = conn.cursor()
      c.execute('INSERT INTO volunteers ("name", "orientation", "status", "created_at", "updated_at") VALUES (?, ?, ?, ?, ?)',
          (request.forms.get("name"), request.forms.get("orientation"), request.forms.get("status"),
           datetime.datetime.now(), datetime.datetime.now() ) )
      new_id = c.lastrowid
    return list_volunteers(message="Added successfully")

@route('/volunteers/<id:int>/edit')
def edit_volunteer_form(id, message=''):
    title = 'Edit Volunteer'
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, date(orientation), status FROM volunteers WHERE id LIKE ?", (id,))
      result = c.fetchone()
    return template('volunteer_edit', title=title, nav=nav, message=message, id=id, values=result)

@route('/volunteers/<id:int>/edit', method='POST')
def edit_volunteer_submit(id):
    if request.forms.get('name') == '':
      return edit_volunteer_form(id, "Please enter a Name")
    if request.forms.get('orientation') == '':
      return edit_volunteer_form(id, "Please select an Orientation date")
    with conn:
      c = conn.cursor()
      c.execute('UPDATE volunteers SET "name" = ?, "orientation" = ?, "status" = ?, "updated_at" = ? where id LIKE ?',
        (request.forms.get('name'), request.forms.get('orientation'), request.forms.get('status'), datetime.datetime.now(), id) )
    return list_volunteers(message="Updated successfully")

@route('/volunteers/<id:int>')
def show_volunteer(id):
    title = 'Show Volunteer'
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, date(orientation), status FROM volunteers WHERE id LIKE ?", (id,))
      result = c.fetchone()
    return template('volunteer_show', title=title, nav=nav, message=message, id=id, values=result)

@route('/volunteers/<id:int>/delete')
def delete_volunteer_confirm(id):
    title = 'Delete Volunteer?'
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, date(orientation), status FROM volunteers WHERE id LIKE ?", (id,))
      result = c.fetchone()
    return template('volunteer_show', title=title, nav=nav, message=message, id=id, values=result, delete=True)

@route('/volunteers/<id:int>/delete', method='POST')
def delete_volunteer_submit(id):
    with conn:
      c = conn.cursor()
      c.execute("DELETE FROM volunteers WHERE id LIKE ?", (id,))
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
run(host="", port=8080, reloader=True, debug=True)
