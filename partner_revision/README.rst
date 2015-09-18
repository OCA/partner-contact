=================
Partner Revisions
=================

Configuration
=============

Access Rights
-------------

The revisions rules must be edited by users with the group ``Revision
Configuration``. The revisions can be applied or canceled only by users
with the group ``Revisions Validations``

Revision Rules
--------------

The revision rules can be configured in ``Sales > Configuration >
Partner Revisions > Revision Fields Rules``. For each partner field, an
action can be defined:

* Auto: the changes made on this field are always applied
* Validate: the changes made on this field must be manually confirmed by
  a 'Revision User' user
* Never: the changes made on this field are always refused

In any case, all the changes made by the users are always applied
directly on the users, but a 'validated' revision is created for the
history.

The supported fields are:

* Char
* Text
* Date
* Datetime
* Integer
* Float
* Boolean
* Many2one

Usage
=====

General case
------------

When users modify the partners, new 'validated' revisions are created so
there is nothing to do.  Addons wanting to create revisions which need a
validation should pass the key ``__revision_rules`` in the context when
they write on the partner.

Finding changesets
------------------

A menu shows all the changesets in ``Sales > Configuration > Partner
Revisions > Partner Revision``.

However, it is more convenient to access them directly from the
partners. Pending revisions can be accessed directly from the top right
of the partners' view.  A new filter on the partners shows the partners
having at least one pending revision.

Handling changesets
-------------------

A revision shows the list of the changes made on a partner. Some of the
changes may be 'Pending', some 'Accepted' or 'Rejected' according to the
revision rules.  The only changes that need an action from the user are
'Pending' changes. When a change is accepted, the value is written on
the user.

The changes view shows the name of the partner's field, the Origin value
and the New value alongside the state of the change. By clicking on the
change in some cases a more detailed view is displayed, for instance,
links for relations can be clicked on.

A button on a changeset allows to apply or reject all the changes at
once.
