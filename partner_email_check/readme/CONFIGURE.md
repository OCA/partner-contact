Install python package email-validator:
`sudo pip install email-validator`.

To not allow multiple partners to have the same email address, use the
"Filter duplicate email
addresses"/`partner_email_check_filter_duplicates` setting.

To validate that email addresses are deliverable (that the hostname
exists), use the "Check deliverability of email
addresses"/`partner_email_check_check_deliverability` setting.

Checks are disabled by default when running under Odoo's test mode. To
enable them anyway in a test, pass the `partner_email_check_force`
context key (e.g. `partner.with_context(partner_email_check_force=True)`).
