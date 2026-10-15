This module was written to extend the functionality of contact types
for a flexible extension.

It adds computed helper fields on `res.partner` (`is_address_readonly`,
`is_individual`, `can_be_parent`, `can_be_child`) that other modules can
override to customize which partners can be parents or children, which
partners get a split name, and when the address fields are readonly.

In the partner form, the module:

- re-adds the address type selection (replaced by a readonly label in
  Odoo 19), so the type can be chosen when creating a contact;
- binds the readonly state of the address fields only to
  `is_address_readonly`, so extension modules control it in one place.
