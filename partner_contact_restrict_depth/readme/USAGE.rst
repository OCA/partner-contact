There is a new system parameter which is called partner_contact_depth. contacts_max_depth

Behaviour:

#. contacts_max_depth = 0, no depth restrictions
#. contacts_max_depth = X, just will be allowed X levels of contacts hierarchy

Example:

#. If contacts_max_depth = 1, If we have Partner0 (depth=0) that his child is Partner1. If we try to add a new child to Partner1(depth=1), Partner2 (depth=2), a Validation Error will be raised as depth from Partner2 is greater that the contacts_max_depth
