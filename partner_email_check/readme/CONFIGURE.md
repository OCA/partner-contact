Install python package email-validator:
`sudo pip install email-validator`.

To not allow multiple partners to have the same email address, use the
"Filter duplicate email
addresses"/`partner_email_check_filter_duplicates` setting.

To validate that email addresses are deliverable (that the hostname
exists), use the "Check deliverability of email
addresses"/`partner_email_check_check_deliverability` setting.

To save `"Name" <address>` as `address` instead of rejecting it, use the
"Clean display name from email addresses"/`partner_email_check_clean_display_name`
setting.
