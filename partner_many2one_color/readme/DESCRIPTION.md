This module lets you flag a contact as *Warning* (yellow) or *Critical* (red),
with an optional message, in the **Notes** tab of the partner form.

Every many2one field pointing to that contact, for example the customer on a
timesheet line, a task or a sales order, then shows the contact's name in that
color, in edit mode as well as in read-only list and kanban cells. The message
is displayed as tooltip, and matching entries in the autocomplete dropdown are
colored too.

Contacts without an own color state inherit the color state and message of
their parent contact: flag a company as *Critical* and all its contacts and
addresses are highlighted in red as well, unless one of them has an own color
state.

The coloring itself is provided by the `web_many2one_color` module; this
module applies it to contacts.
