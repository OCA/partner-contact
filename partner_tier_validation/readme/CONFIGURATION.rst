The approval rules can be configured to suit particular use cases.
A default validation rule is provided out of the box,
that can be used as a starting point fot this configuration.

This configuration is done at
*Settings / Technical / Tier Validations / Tier Definition*.

Also relevant is the configuration on the default Stage
for new Contacts/Partners.
This can be set at *Contacts / Configuration / Contact Stage*,
setting the "Default Sate" field on the appropriate Stage record.

Changing some fields will trigger a new request for validation.
This list of fields can be customized extending ``_partner_tier_revalidation_fields``.
By default these fields are:

- Company Type (Individual or Company)
- Parent Company
- Tax ID
- State
- Country
- Fiscal Position
- Account Receivable
- Account Payable
