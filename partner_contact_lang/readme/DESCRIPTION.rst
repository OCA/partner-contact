Odoo by default propagate language field to the created contacts from their
form, but it doesn't allow to change it once created.

This module fills this gap, and also provides other facilities for the
contact language management:

#. Put the language of the parent company when the contact doesn't have a
language and this parent company is assigned.
#. When the company changes the language, it fills with the same language all
the contacts that don't have any.
