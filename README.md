vets
====

Volunteer Effort Tracking System

Originally designed for our local SPCA to track its volunteer hours,
this project is being re-written to be more lightweight and generic.

The core functionality consists of managing volunteers' names, and
orientation dates, as well as providing a sign-in/ sign-out page where
volunteers can select a category for the time they spent volunteering.
On a periodic basis, the volunteer coordinator can run reports to display
information like total time a volunteer contributed over a given time
period or total time spent on a given activity 
(e.g. office work, dog walking, cat socialization).

Homepage and documentation: https://github.com/vets/vets

status
------
Initial re-write from original Rails version is about done.
At this point should mostly be final tweaks and optimizations based
on feedback from anyone willing to look the project over.

deployment
----------
VETS includes a copy of bottle.py in vendor/ that is known to work
(though it is likely newer versions also work). All you should need
on a machine is Python 2.5+ and possibly sqlite3 if you want to be
able to query/edit the database outside of the application.

* To initialize the database

    db/init_db.py -c db/development.sqlite3

* To start the server

    vets.py

* Browse to http://localhost:8080