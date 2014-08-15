#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VETS is a Volunteer Effort Tracking System

Homepage and documentation: https://github.com/vets/vets/

Copyright (c) 2014, Kevin Worth
License: MIT (see LICENSE for details)
"""
__author__  = 'Kevin Worth'
__version__ = '0.07-dev'
__license__ = 'MIT'

import os, re, sqlite3, datetime, ConfigParser
from vendor.bottle import route, run, template, get, post, request, error, install, static_file, response


# Check in/out handlers

@route('/')
@route('/home')
@route('/checkin')
def check_in_form(message='', title='Checked-in Volunteers'):
    with conn:
      c = conn.cursor()
      c.execute("SELECT hours.id, volunteer_id, volunteers.name AS volunteer, strftime('%m-%d %H:%M',start), end FROM hours JOIN volunteers ON hours.volunteer_id=volunteers.id WHERE end is null ORDER BY volunteer")
      hours = c.fetchall()
      c.execute("SELECT id, name FROM volunteers WHERE status = 'active' ORDER BY name")
      volunteers = c.fetchall()
    return template('check_in', title=title, admin=request.get_cookie("admin"), message=message, rows=hours, volunteers=volunteers)

@route('/checkin', method='POST')
def check_in_submit():
    if request.forms.get('volunteer_id') == '':
      return check_in_form(message="Please select your Name")
    with conn:
      c = conn.cursor()
      c.execute('INSERT INTO hours ("volunteer_id", "start", "created_at", "updated_at") VALUES (?, ?, ?, ?)',
          (request.forms.get("volunteer_id"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ) )
      new_id = c.lastrowid
    return check_in_form(message="Checked In Successfully!")

@route('/checkout/<id:int>')
def check_out_form(id, message='', title='Check Out'):
    now = datetime.datetime.now()
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, volunteer_id, activity_id, start, end FROM hours WHERE id LIKE ?", (id,))
      result = c.fetchone()
      c.execute("SELECT id, name FROM volunteers WHERE id = ?", (result['volunteer_id'],) )
      volunteer = c.fetchone()
      c.execute("SELECT id, name FROM activities WHERE status = 'active' ORDER BY name")
      activities = c.fetchall()
    start = datetime.datetime.strptime(result['start'], "%Y-%m-%d %H:%M:%S")
    return template('check_out', title=title, admin=request.get_cookie("admin"), message=message, now=now,
                    volunteer=volunteer, activities=activities, id=id, values=result, start=start)

@route('/checkout/<id:int>', method='POST')
def check_out_submit(id):
    if request.forms.get('activity_id') == '':
      return check_out_form(id, message="Please select an Activity")
    start = datetime.datetime.strptime("{} {}:{} {}".format(request.forms.get("start_date"),
                                                            request.forms.get("start_hour"),
                                                            request.forms.get("start_minute"),
                                                            request.forms.get("start_ampm")),
                                      "%Y-%m-%d %I:%M %p")
    end = datetime.datetime.strptime("{} {}:{} {}".format(request.forms.get("end_date"),
                                                          request.forms.get("end_hour"),
                                                          request.forms.get("end_minute"),
                                                          request.forms.get("end_ampm")),
                                     "%Y-%m-%d %I:%M %p")
    if (end - start).total_seconds() < 0:
      return check_out_form(id, message="Check-Out time must be after Check-In time")
    with conn:
      c = conn.cursor()
      c.execute('UPDATE hours SET "activity_id" = ?, "start" = ?, "end" = ?, "updated_at" = ? where id LIKE ?',
        (request.forms.get('activity_id'), start, end, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id) )
    return check_in_form(message="Checked Out Successfully!")


# Hours handlers

@route('/hours')
def list_hours(message='', title='Hours Report', start=datetime.date.today(), end=(datetime.date.today()+datetime.timedelta(days=1)), group_by=''):
    with conn:
      c = conn.cursor()
      if group_by == '':
        c.execute("SELECT hours.id, volunteers.name AS volunteer, activities.name AS activity, strftime('%m-%d %H:%M',start), strftime('%m-%d %H:%M',end), (strftime('%s',end)-strftime('%s',start))/3600.0 AS totalHours FROM hours JOIN volunteers ON hours.volunteer_id=volunteers.id LEFT OUTER JOIN activities ON hours.activity_id=activities.id WHERE start >= ? AND end <= ? ORDER BY start", (start, end))
      elif group_by == 'volunteer':
        c.execute("SELECT volunteers.name AS volunteer, SUM(strftime('%s',end)-strftime('%s',start))/3600.0 AS totalHours FROM hours JOIN volunteers ON hours.volunteer_id=volunteers.id WHERE start >= ? AND end <= ? GROUP BY volunteer_id ORDER BY volunteer", (start, end))
      elif group_by == 'activity':
        c.execute("SELECT activities.name AS activity, SUM(strftime('%s',end)-strftime('%s',start))/3600.0 AS totalHours FROM hours JOIN activities ON hours.activity_id=activities.id WHERE start >= ? AND end <= ? GROUP BY activity_id ORDER BY activity", (start, end))
      hours = c.fetchall()
    return template('hour_list', title=title, admin=request.get_cookie("admin"), message=message, rows=hours, start=start, end=end, group_by=group_by)

@route('/hours', method='POST')
def list_hours_submit():
    return list_hours(start=request.forms.get("start"), end=request.forms.get("end"), group_by=request.forms.get("group_by"))

@route('/hours/<id:int>/delete')
def delete_hour_confirm(id, title='Delete Record?'):
    with conn:
      c = conn.cursor()
      c.execute("SELECT hours.id, volunteers.name AS volunteer, activities.name AS activity, strftime('%m-%d %H:%M',start), strftime('%m-%d %H:%M',end) FROM hours JOIN volunteers ON hours.volunteer_id=volunteers.id LEFT OUTER JOIN activities ON hours.activity_id=activities.id WHERE hours.id LIKE ?", (id,))
      result = c.fetchone()
    return template('hour_delete', title=title, admin=request.get_cookie("admin"), message=message, id=id, values=result, delete=True)

@route('/hours/<id:int>/delete', method='POST')
def delete_hour_submit(id):
    with conn:
      c = conn.cursor()
      c.execute("DELETE FROM hours WHERE id LIKE ?", (id,))
    return list_hours(message="Deleted successfully")


# Volunteer handlers

@route('/volunteers')
@route('/volunteers/<status:re:active|inactive>')
def list_volunteers(message='', status='active', title='Volunteers'):
    title = '%s Volunteers' % (status.title())
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, date(orientation) as orientation, status FROM volunteers WHERE status = ? ORDER BY name", (status,))
      result = c.fetchall()
    return template('volunteer_list', title=title, admin=request.get_cookie("admin"), message=message, rows=result, status=status)

@route('/volunteers/new')
def new_volunteer_form(message='', title='New Volunteer'):
    today = datetime.date.today()
    return template('volunteer_form', title=title, admin=request.get_cookie("admin"), message=message, today=today)

@route('/volunteers/new', method='POST')
def new_volunteer_submit():
    if request.forms.get('name') == '':
      return new_volunteer_form(message="Please enter a Name")
    if request.forms.get('orientation') == '':
      return new_volunteer_form(message="Please select an Orientation date")
    with conn:
      c = conn.cursor()
      c.execute('INSERT INTO volunteers ("name", "orientation", "status", "created_at", "updated_at") VALUES (?, ?, ?, ?, ?)',
          (request.forms.get("name"), request.forms.get("orientation"), request.forms.get("status"),
           datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ) )
      new_id = c.lastrowid
    return list_volunteers(message="Added successfully")

@route('/volunteers/<id:int>/edit')
def edit_volunteer_form(id, message='', title='Edit Volunteer'):
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, date(orientation) as orientation, status FROM volunteers WHERE id LIKE ?", (id,))
      result = c.fetchone()
    return template('volunteer_form', title=title, admin=request.get_cookie("admin"), message=message, id=id, values=result)

@route('/volunteers/<id:int>/edit', method='POST')
def edit_volunteer_submit(id):
    if request.forms.get('name') == '':
      return edit_volunteer_form(id, message="Please enter a Name")
    if request.forms.get('orientation') == '':
      return edit_volunteer_form(id, message="Please select an Orientation date")
    with conn:
      c = conn.cursor()
      c.execute('UPDATE volunteers SET "name" = ?, "orientation" = ?, "status" = ?, "updated_at" = ? where id LIKE ?',
        (request.forms.get('name'), request.forms.get('orientation'), request.forms.get('status'), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id) )
    return list_volunteers(message="Updated successfully")


# Activity handlers

@route('/activities')
@route('/activities/<status:re:active|inactive>')
def list_activities(message='', status='active', title='Activities'):
    title = '%s Activities' % (status.title())
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, status FROM activities WHERE status = ? ORDER BY name", (status,))
      result = c.fetchall()
    return template('activity_list', title=title, admin=request.get_cookie("admin"), message=message, rows=result, status=status)

@route('/activities/new')
def new_activity_form(message='', title='New Activity'):
    return template('activity_form', title=title, admin=request.get_cookie("admin"), message=message)

@route('/activities/new', method='POST')
def new_activity_submit():
    if request.forms.get('name') == '':
      return new_activity_form(message="Please enter a Name")
    with conn:
      c = conn.cursor()
      c.execute('INSERT INTO activities ("name", "status", "created_at", "updated_at") VALUES (?, ?, ?, ?)',
          (request.forms.get("name"), request.forms.get("status"),
           datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ) )
      new_id = c.lastrowid
    return list_activities(message="Added successfully")

@route('/activities/<id:int>/edit')
def edit_activity_form(id, message='', title='Edit Activity'):
    with conn:
      c = conn.cursor()
      c.execute("SELECT id, name, status FROM activities WHERE id LIKE ?", (id,))
      result = c.fetchone()
    return template('activity_form', title=title, admin=request.get_cookie("admin"), message=message, id=id, values=result)

@route('/activities/<id:int>/edit', method='POST')
def edit_activity_submit(id):
    if request.forms.get('name') == '':
      return edit_activity_form(id, message="Please enter a Name")
    with conn:
      c = conn.cursor()
      c.execute('UPDATE activities SET "name" = ?, "status" = ?, "updated_at" = ? where id LIKE ?',
        (request.forms.get('name'), request.forms.get('status'), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id) )
    return list_activities(message="Updated successfully")


# Miscellaneous Handlers

@route('/admin')
def admin_login_form(message=''):
  return template('admin_login', title="Admin Log-in", admin=request.get_cookie("admin"), message=message)

@route('/admin', method='POST')
def admin_login_submit(message=''):
  password = request.forms.get('password')
  if password == admin_password:
    response.set_cookie("admin", "true")
    return template('message_only', title='Admin Logged In', admin='true', message='Admin Log-in Successful')
  else:
    return admin_login_form(message="Bad Password")

@route('/logout')
def admin_logout(message=''):
  response.set_cookie("admin", "false", expires=0)
  return template('message_only', title='Admin Logged Out', admin='', message='Admin Log-out Successful')

@route('/backup')
def db_backup():
  filename = "db/backups/backup-{}.sql".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
  with open(filename, 'w') as f:
    with conn:
      for line in conn.iterdump():
        f.write("{}\n".format(line))
  return template('message_only', title='Database Backup', admin=request.get_cookie("admin"), message='Database Backed up to {}'.format(filename))

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')

# TODO find/make a logo
#@route('/favicon.ico')
def send_favicon():
    return static_file('favicon.png', root='static')


# Stuff to parse configs and handle databases

# Values for a default config file
cfg_file       = "vets.cfg"
db_file        = "db/test.sqlite3"
admin_password = "pizza"
host           = ""
port           = 8080
debug          = True

def create_default_config():
  with open(cfg_file, 'w') as f:
    f.write("# Change values to suit your needs\n# Don't use a valuable password since it's stored and send in the clear\n")
    Config.add_section('VETS')
    Config.set('VETS', 'dbFile', db_file)
    Config.set('VETS', 'adminPassword', admin_password)
    Config.set('VETS', 'host', host)
    Config.set('VETS', 'port', port)
    Config.set('VETS', 'debug', debug)
    Config.write(f)
  
def create_empty_database():
  with sqlite3.connect(db_file) as conn:
    c = conn.cursor()
    c.execute('CREATE TABLE "volunteers" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "name" VARCHAR(255), "orientation" TIMESTAMP, "status" VARCHAR(255), "created_at" TIMESTAMP, "updated_at" TIMESTAMP)')
    c.execute('CREATE TABLE "activities" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "name" VARCHAR(255), "status" VARCHAR(255), "created_at" TIMESTAMP, "updated_at" TIMESTAMP)')
    c.execute('CREATE TABLE "hours" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "volunteer_id" INTEGER, "start" TIMESTAMP, "end" TIMESTAMP, "activity_id" INTEGER, "created_at" TIMESTAMP, "updated_at" TIMESTAMP)')

# Check and parse config file
Config = ConfigParser.ConfigParser()
if os.path.isfile(cfg_file) == False:
  print("Creating default values in {}".format(cfg_file))
  create_default_config()
Config.read(cfg_file)
db_file        = Config.get('VETS', 'dbFile')
admin_password = Config.get('VETS', 'adminPassword')
host           = Config.get('VETS', 'host')
port           = Config.get('VETS', 'port')
debug          = Config.get('VETS', 'debug')

# Check and load database file
if os.path.isfile(db_file) == False:
  print("Creating empty database in {}".format(db_file))
  create_empty_database()
conn = sqlite3.connect(db_file)
conn.row_factory = sqlite3.Row


# Actually start the server
run(host=host, port=port, reloader=debug, debug=debug)
