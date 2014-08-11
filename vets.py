#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VETS is a Volunteer Effort Tracking System

Homepage and documentation: https://github.com/vets/vets/

Copyright (c) 2014, Kevin Worth
License: MIT (see LICENSE for details)
"""
__author__  = 'Kevin Worth'
__version__ = '0.03-dev'
__license__ = 'MIT'

import os, re, sqlite3, datetime
from vendor.bottle import route, run, template, get, post, request, error, install, static_file, response

#Database settings
conn = sqlite3.connect("db/test.sqlite3")
conn.row_factory = sqlite3.Row
datetime.microseconds = False

#Globals for commonly passed stuff
nav = ['Hours', 'Volunteers', 'Categories']
message = ''

#Cheesy way to hide admin controls most of the time
global admin
admin = False

# Hour handlers

@route('/')
@route('/hours')
def check_in(message=''):
    title = 'Checked-in Volunteers'
    with conn:
      c = conn.cursor()
      #c.execute("SELECT id, volunteer_id, category_id, start, end FROM hours WHERE end = ? ORDER BY start", ("",))
      #c.execute("SELECT hours.id, volunteer_id, volunteers.name, category_id, categories.name, start, end FROM hours JOIN volunteers ON hours.volunteer_id=volunteers.id JOIN categories ON hours.category_id=categories.id WHERE end = ? ORDER BY start", ("",))
      c.execute("SELECT hours.id, volunteer_id, volunteers.name AS volunteer, strftime('%m-%d %H:%M',start), end FROM hours JOIN volunteers ON hours.volunteer_id=volunteers.id WHERE end is null ORDER BY start")
      result = c.fetchall()
      c.execute("SELECT id, name FROM volunteers WHERE status = 'active' ORDER BY name")
      volunteers = c.fetchall()
    return template('hour_list', title=title, nav=nav, message=message, rows=result, volunteers=volunteers)

@route('/hours', method='POST')
def check_in_submit():
    if request.forms.get('volunteer_id') == '':
      return check_in("Please select your Name")
    with conn:
      c = conn.cursor()
      c.execute('INSERT INTO hours ("volunteer_id", "start", "created_at", "updated_at") VALUES (?, ?, ?, ?)',
          (request.forms.get("volunteer_id"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ) )
      new_id = c.lastrowid
    return check_in(message="Checked In Successfully!")

# Only really used by admin for creating old records
@route('/hours/new')
def new_hour_form(message=''):
    title = 'Check In'
    now = datetime.datetime.now()
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name FROM volunteers WHERE status = 'active' ORDER BY name")
      volunteers = c.fetchall()
      c.execute("SELECT id, name FROM categories WHERE status = 'active' ORDER BY name")
      categories = c.fetchall()
    return template('hour_edit', title=title, nav=nav, message=message, now=now, volunteers=volunteers, categories=categories)

@route('/hours/new', method='POST')
def new_hour_submit():
    if request.forms.get('volunteer_id') == '':
      return new_hour_form("Please select your Name")
    startstring = datetime.datetime.strptime("{} {}:{} {}".format(request.forms.get("start_date"),
                                                                  request.forms.get("start_hour"),
                                                                  request.forms.get("start_minute"),
                                                                  request.forms.get("start_ampm")),
                                             "%Y-%m-%d %I:%M %p")
    with conn:
      c = conn.cursor()
      c.execute('INSERT INTO hours ("volunteer_id", "start", "created_at", "updated_at") VALUES (?, ?, ?, ?)',
          (request.forms.get("volunteer_id"), startstring,
          datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ) )
      new_id = c.lastrowid
    return check_in(message="Checked In Successfully!")

@route('/hours/<id:int>/edit')
def edit_hour_form(id, message=''):
    title = 'Check Out'
    now = datetime.datetime.now()
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, volunteer_id, category_id, start, end FROM hours WHERE id LIKE ?", (id,))
      result = c.fetchone()
      c.execute("SELECT id, name FROM volunteers WHERE status = 'active' ORDER BY name")
      volunteers = c.fetchall()
      c.execute("SELECT id, name FROM categories WHERE status = 'active' ORDER BY name")
      categories = c.fetchall()
    start = datetime.datetime.strptime(result['start'], "%Y-%m-%d %H:%M:%S")
    return template('hour_edit', title=title, nav=nav, message=message, now=now, volunteers=volunteers, categories=categories, id=id, values=result, start=start)

@route('/hours/<id:int>/edit', method='POST')
def edit_hour_submit(id):
    if request.forms.get('category_id') == '':
      return edit_hour_form(id, "Please select an Activity")
    startstring = datetime.datetime.strptime("{} {}:{} {}".format(request.forms.get("start_date"),
                                                                  request.forms.get("start_hour"),
                                                                  request.forms.get("start_minute"),
                                                                  request.forms.get("start_ampm")),
                                             "%Y-%m-%d %I:%M %p")
    endstring = datetime.datetime.strptime("{} {}:{} {}".format(request.forms.get("end_date"),
                                                                request.forms.get("end_hour"),
                                                                request.forms.get("end_minute"),
                                                                request.forms.get("end_ampm")),
                                           "%Y-%m-%d %I:%M %p")
    with conn:
      c = conn.cursor()
      c.execute('UPDATE hours SET "category_id" = ?, "start" = ?, "end" = ?, "updated_at" = ? where id LIKE ?',
        (request.forms.get('category_id'), startstring, endstring, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id) )
    return check_in(message="Checked Out Successfully!")

    with conn:
      c = conn.cursor()
      c.execute('INSERT INTO hours ("volunteer_id", "start", "created_at", "updated_at") VALUES (?, ?, ?, ?)',
          (request.forms.get("volunteer_id"), datestring,
          datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ) )
      new_id = c.lastrowid
    return check_in(message="Checked In Successfully!")
  

@route('/hours/<id:int>')
def show_hour(id):
    title = 'Show Record'
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, volunteer_id, category_id, start, end FROM hours WHERE id LIKE ?", (id,))
      result = c.fetchone()
    return template('hour_show', title=title, nav=nav, message=message, id=id, values=result)

@route('/hours/<id:int>/delete')
def delete_hour_confirm(id):
    title = 'Delete Record?'
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, volunteer_id, category_id, start, end FROM hours WHERE id LIKE ?", (id,))
      result = c.fetchone()
    return template('hour_show', title=title, nav=nav, message=message, id=id, values=result, delete=True)

@route('/hours/<id:int>/delete', method='POST')
def delete_hour_submit(id):
    with conn:
      c = conn.cursor()
      c.execute("DELETE FROM hours WHERE id LIKE ?", (id,))
    return check_in(message="Deleted successfully")


# Volunteer handlers

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
    today = datetime.date.today()
    return template('volunteer_edit', title=title, nav=nav, message=message, today=today)

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
           datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ) )
      new_id = c.lastrowid
    return list_volunteers(message="Added successfully")

@route('/volunteers/<id:int>/edit')
def edit_volunteer_form(id, message=''):
    title = 'Edit Volunteer'
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, date(orientation) as orientation_date, status FROM volunteers WHERE id LIKE ?", (id,))
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
        (request.forms.get('name'), request.forms.get('orientation'), request.forms.get('status'), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id) )
    return list_volunteers(message="Updated successfully")

@route('/volunteers/<id:int>')
def show_volunteer(id):
    title = 'Show Volunteer'
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, date(orientation), status FROM volunteers WHERE id LIKE ?", (id,))
      result = c.fetchone()
    return template('volunteer_show', title=title, nav=nav, message=message, id=id, values=result)

# TODO Disable volunteer delete (set status=inactive instead) since it will cause broken hours entries
#
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


# Category handlers

@route('/categories')
@route('/categories/<status:re:active|inactive>')
def list_categories(message='', status='active'):
    title = '%s Categories' % (status.title())
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, status FROM categories WHERE status = ? ORDER BY name", (status,))
      result = c.fetchall()
    return template('category_list', title=title, nav=nav, message=message, rows=result, status=status)

@route('/categories/new')
def new_category_form(message=''):
    title = 'New Category'
    return template('category_edit', title=title, nav=nav, message=message)

@route('/categories/new', method='POST')
def new_category_submit():
    if request.forms.get('name') == '':
      return new_category_form("Please enter a Name")
    with conn:
      c = conn.cursor()
      c.execute('INSERT INTO categories ("name", "status", "created_at", "updated_at") VALUES (?, ?, ?, ?)',
          (request.forms.get("name"), request.forms.get("status"),
           datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ) )
      new_id = c.lastrowid
    return list_categories(message="Added successfully")

@route('/categories/<id:int>/edit')
def edit_category_form(id, message=''):
    title = 'Edit Category'
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, status FROM categories WHERE id LIKE ?", (id,))
      result = c.fetchone()
    return template('category_edit', title=title, nav=nav, message=message, id=id, values=result)

@route('/categories/<id:int>/edit', method='POST')
def edit_category_submit(id):
    if request.forms.get('name') == '':
      return edit_category_form(id, "Please enter a Name")
    with conn:
      c = conn.cursor()
      c.execute('UPDATE categories SET "name" = ?, "status" = ?, "updated_at" = ? where id LIKE ?',
        (request.forms.get('name'), request.forms.get('status'), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id) )
    return list_categories(message="Updated successfully")

@route('/categories/<id:int>')
def show_category(id):
    title = 'Show Category'
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, status FROM categories WHERE id LIKE ?", (id,))
      result = c.fetchone()
    return template('category_show', title=title, nav=nav, message=message, id=id, values=result)

# TODO Disable category delete (set status=inactive instead) since it will cause broken hours entries
#
@route('/categories/<id:int>/delete')
def delete_category_confirm(id):
    title = 'Delete Category?'
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, status FROM categories WHERE id LIKE ?", (id,))
      result = c.fetchone()
    return template('category_show', title=title, nav=nav, message=message, id=id, values=result, delete=True)

@route('/categories/<id:int>/delete', method='POST')
def delete_category_submit(id):
    with conn:
      c = conn.cursor()
      c.execute("DELETE FROM categories WHERE id LIKE ?", (id,))
    return list_categories(message="Deleted successfully")


# Miscellaneous Handlers

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
