This module integrate automatically in all of the view `res.partner`

## Bypassing the checks for a single operation

The checks run on every `res.partner` create and write. That is what you want
for an address a user typed, but not for one your code did not collect from a
user: the incoming mail gateway creates a partner for the sender of every
message it accepts, and bulk senders routinely send from a subdomain that
publishes no MX record, so a deliverability failure there discards the message
rather than improving anyone's data.

Two context keys turn a check off for one operation:

```python
# Store the address even though its domain accepts no mail.
partner.with_context(partner_email_check_skip_deliverability=True).write(vals)

# Store it without validating or normalizing it at all.
partner.with_context(partner_email_check_skip_syntax=True).write(vals)
```

`partner_email_check_skip_deliverability` keeps validation and normalization and
skips only the DNS lookup. `partner_email_check_skip_syntax` skips both, exactly
as disabling the company setting does.
