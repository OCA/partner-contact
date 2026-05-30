Install python package email-validator:
`sudo pip install email-validator`.

To not allow multiple partners to have the same email address, use the
"Filter duplicate email
addresses"/`partner_email_check_filter_duplicates` setting.

When duplicate filtering is enabled, the "Duplicate email
scope"/`partner_email_check_duplicate_scope` setting controls how widely
addresses must be unique:

- *Across all companies* (default): an email address may only be used once in
  the whole database.
- *Within the same company*: the same email address may be reused by a partner
  of another company, but must stay unique inside each company.

To validate that email addresses are deliverable (that the hostname
exists), use the "Check deliverability of email
addresses"/`partner_email_check_check_deliverability` setting.
