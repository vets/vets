vets
====

Volunteer Effort Tracking System

Originally designed for our local SPCA to track its volunteer hours,
this project is being re-written to be more lightweight and generic.

The core functionality consists of managing volunteers' names, and
orientation dates, as well as providing a sign-in/ sign-out page where
volunteers can select a category for the time they spent volunteering.
On a periodic basis, volunteer coordinators can run reports to display
information like total time a volunteer contributed over a given time
period or total time spent on a given category 
(e.g. office work, dog walking, cat socialization).

Homepage and documentation: https://github.com/vets/vets

status
------
Undergoing major re-write from Rails 5 years ago including
a bunch of functionality that didn't get utilized to bottle.py
which should remain focused, lightweight, and maintainable.

Initial versions are going to look ugly as the priority will
be getting something basic that works, then iterating on
improvements for cleaner, faster code.

deployment
----------
VETS includes a copy of bottle.py in vendor/ that is known to work
(though it is likely newer versions also work). All you should need
on a machine is Python (known to work with 2.7).
