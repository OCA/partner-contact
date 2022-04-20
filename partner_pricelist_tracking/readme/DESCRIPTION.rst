When we change the country or the state of the partner, Odoo tries to match a proper
pricelist for the country, which will be the first it finds with a country group
containing such country. The user could be unaware of this change (that could be right
or not) and the partner would be left with a wrong pricelist. So we enable traceability
to at least be able to log those changes and give the users the chance to amend them.
We could also want to log manual changes overtime.
