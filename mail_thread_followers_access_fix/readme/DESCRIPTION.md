Stops Odoo from crashing when a document has a follower the current user
is not allowed to read.

`mail.thread`'s `message_partner_ids` (the computed field behind the
"Followers" panel) is built with a plain `browse()` of every follower's
partner id, with no regard for whether the current user can actually read
each one. That is fine by default, because stock Odoo never hides one
internal user's contact from another. But the moment *any* module adds a
record rule that can hide a `res.partner` from some users (a company- or
role-based visibility restriction, for example), opening -- or even just
listing -- a document that has one of those hidden contacts as a follower
raises an `AccessError` and the whole read fails, because Odoo's field
conversion needs to check each follower's `active` field to build the
recordset, and that check enforces record rules.

This module recomputes the visible follower list through a `search()`
instead of a raw `browse()`: `search()` already applies record rules and
simply omits what the current user cannot see, rather than crashing. A
document's follower list becomes "every follower I'm allowed to see",
which degrades gracefully instead of breaking the page.

This is a general-purpose compatibility fix, useful any time a
`res.partner` visibility restriction is in place -- it does not depend on
any specific one. In this repository it is paired with
`partner_multi_company_restrict` and `partner_hide_admin_contact`.
