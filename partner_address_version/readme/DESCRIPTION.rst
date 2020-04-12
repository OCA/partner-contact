This module allows you to manage versions for partner addresses.

A list of fields are defined for versioning. These are immutable once set, and force the user to create a new partner
if they want to change one of these fields.

This forces historical consistency. For example, the moment you confirm a
sale order, you might want to lock the address of that sale order instead of having it
change everytime that partner is modified (see e.g sale_partner_version).
