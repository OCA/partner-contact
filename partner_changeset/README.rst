==================
Partner Changesets
==================

Configuration
=============

Access Rights
-------------

The changesets rules must be edited by users with the group ``Changesets
Configuration``. The changesets can be applied or canceled only by users
with the group ``Changesets Validations``

Changesets Rules
----------------

The changesets rules can be configured in ``Sales > Configuration >
Partner Changesets > Fields Rules``. For each partner field, an
action can be defined:

* Auto: the changes made on this field are always applied
* Validate: the changes made on this field must be manually confirmed by
  a 'Changesets User' user
* Never: the changes made on this field are always refused

In any case, all the changes made by the users are always applied
directly on the users, but a 'validated' changeset is created for the
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

When users modify the partners, new 'validated' changeset are created so
there is nothing to do.  Addons wanting to create changeset which need a
validation should pass the key ``_changeset_rules`` in the context when
they write on the partner.

The keys a caller should pass in the context are:
* ``__changeset_rules``: activate the rules for the changesets
* ``__changeset_rules_source_model``: name of the model which asks for
  the change
* ``__changeset_rules_source_id``: id of the record which asks for the
  change

The source is used for the application of the rules, it is also stored
on the changeset for information.

Finding changesets
------------------

A menu shows all the changesets in ``Sales > Configuration > Partner
Changesets > Changesets``.

However, it is more convenient to access them directly from the
partners. Pending changesets can be accessed directly from the top right
of the partners' view.  A new filter on the partners shows the partners
having at least one pending changeset.

Handling changesets
-------------------

A changeset shows the list of the changes made on a partner. Some of the
changes may be 'Pending', some 'Accepted' or 'Rejected' according to the
changeset rules.  The only changes that need an action from the user are
'Pending' changes. When a change is accepted, the value is written on
the user.

The changes view shows the name of the partner's field, the Origin value
and the New value alongside the state of the change. By clicking on the
change in some cases a more detailed view is displayed, for instance,
links for relations can be clicked on.

A button on a changeset allows to apply or reject all the changes at
once.
