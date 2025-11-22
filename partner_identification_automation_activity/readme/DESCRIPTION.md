This module extends the partner identification automation functionality by automatically creating mail activities when identification records transition to the 'to_renew' (pending) status.

Features
========
* Automatically creates a mail activity when an ID record status changes to 'pending'
* Assigns the activity to the responsible user defined in the category (or to current user if none)
* Calculates deadline based on renewal lead time settings
* Prevents duplicate activities for the same record
* Optionally creates a mail activity for an initial check when a new identification record is created.
