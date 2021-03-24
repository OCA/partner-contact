The approval rules can be configured to suit particular use cases.
A default validation rule is provided out of the box,
that can be used as a starting point fot this configuration.

This configuration is done at
*Settings > Technical > Tier Validations > Tier Definition*.

Note that, since Contacts start as archived records,
the *Definition Domain* must include ``"|",["active","=",True],["active","=",False]``.
Otherwise the validation rule won't apply correctly in new records.
