Hides a system administrator's contact from regular internal users, in
Contacts.

Odoo's standard `res.partner` record rule always shows contacts linked to
an internal user (`partner_share = False`), including administrators, so
that "assigned to" pickers and similar widgets keep working. This means
any internal user, however junior, can see (and interact with) the
contact record of a system administrator: their email, phone, address,
and any other personal data on file.

This module hides a system administrator's contact (any user holding the
*Administration / Settings* group, `base.group_system`) from a regular
internal user. Administrators are unaffected: they keep seeing every
contact, including other administrators.

This is unrelated to multi-company: it applies the same way whether the
database has one company or many. It composes cleanly with
`partner_multi_company_restrict` (or any other company-scoping rule) if
both are installed, since record rules on the same model without a
specific group combine with a logical AND.

The restriction can be turned off from *Settings > General Settings >
Contacts* if it breaks a legitimate use case, such as adding an
administrator as a follower on a shared document.
