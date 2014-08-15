vets
====
Volunteer Effort Tracking System

Originally designed for our local SPCA
(Society for the Prevention of Cruelty to Animals) to track its volunteer
hours, this project has been re-written to be more lightweight and generic
for long-term use there and possibly at other interested non-profits.

The core functionality consists of managing volunteers' names, and
orientation dates, as well as providing a sign-in/sign-out page where
volunteers can select a category for the time they spent volunteering.

When needed, an "admin" (volunteer coordinator) can run reports to display
information like total time a volunteer contributed over a given time
period or total time spent on a given activity
(e.g. office work, dog walking, cat socialization).

A simple "backup" link that dumps the database out to disk is also
included with the hope that risking filling up disk space is better
than not having backups at all. The backups are simple .sql files 
that could be cat'ed into sqlite3 to re-create the database quickly.

Homepage and documentation: https://github.com/vets/vets

status
------
Most major functionality and features I'm looking to implement are about done.
At this point should mostly be final tweaks and optimizations based
on feedback from anyone willing to look the project over.

deployment
----------
VETS includes a copy of bottle.py in vendor/ that is known to work
(though it is likely newer versions also work). All you should need
on a machine is [Python](https://www.python.org/) 2.5+ and possibly
[sqlite3](http://www.sqlite.org/), but only if you want to be
able to query/edit the database outside of the application using the
sqlite3 command-line tool.

* Start the server
  * `vets.py`
* Browse to http://localhost:8080

The first time you run the server, a default vets.cfg file and empty
database will be created. You can edit vets.cfg to change settings
as you like.

You can deploy this on Windows easily using
[Portable Python](http://portablepython.com)
(2.7.6.1 has been verified to work but newer ones are probably ok too).
Simply do a minimal install (about 50MB) and move the contents of the App
directory to somewhere like C:\vets\python, and run
`C:\vets> python\python.exe vets.py`

Also be aware that VETS uses some HTML5 elements (e.g. date picker),
so for the best experience, use something that supports HTML5 like 
[Chrome](https://www.google.com/intl/en-US/chrome/browser/)

some screenshots
----------------

![Check In](/docs/images/checkin.png?raw=true)
![Check Out](/docs/images/checkout.png?raw=true)
![Admin Log-In](/docs/images/admin.png?raw=true)
![Volunteers](/docs/images/volunteers.png?raw=true)
![Activities](/docs/images/activities.png?raw=true)
![Backup](/docs/images/backup.png?raw=true)
![Hours Report](/docs/images/hours.png?raw=true)
![Hours Report By Volunteer](/docs/images/hours-by-volunteer.png?raw=true)
![Hours Report By Activity](/docs/images/hours-by-activity.png?raw=true)
