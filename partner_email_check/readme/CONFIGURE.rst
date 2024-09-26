Install python package email-validator: ``sudo pip install email-validator``.

To not allow multiple partners to have the same email address, use the
"Filter duplicate email addresses"/``partner_email_check_filter_duplicates``
setting.

In this case, there is also an option to ignore User emails in this duplicate check.
This can be useful in the case you want to allow Users with the same email as existing
Customers or Suppliers.

To validate that email addresses are deliverable (that the hostname exists),
use the "Check deliverability of email addresses"/``partner_email_check_check_deliverability``
setting.
