Configure all ID types you need in Contacts \> Configuration \> Partner
ID Categories. For example, we create a category 'Driver License':

Name:  
Name of this ID type. For example, 'Driver License'

Code:  
Code, abbreviation or acronym of this ID type. For example,
'driver_license'

Scheme:  
Optional code identifying this ID type in an external coding scheme (for
example the Peppol ICD code '0088' for GLN, used for EDI/UBL output).
Falls back to `Code` when not set - only needed when `Code` (used for
other purposes, e.g. internal categorization) differs from the code an
external system expects.

By default, two different ID Categories can share the same `Scheme`. To
forbid this, enable "Enforce unique ID category scheme" on the company
(Settings \> Companies \> a company \> Partner Identification). Once
enabled, saving an ID Category whose `Scheme` is already used by another
one raises a validation error. Categories with no `Scheme` set never
conflict, even when this is enabled.

Python validation code:  
Optional python code called to validate ID numbers of this ID type. This
functionality can be overridden by setting `id_no_validate` to `True` in
the context, such as:

``` python
partner.with_context(id_no_validate=True).write({
   'name': 'Bad Value',
   'category_id': self.env.ref('id_category_only_numerics').id,
})
```
