The purpose of this module is to gather generic partner methods.
It avoids to grow up excessively the number of modules in Odoo
for small features.

Add methods to Partner model like `_get_split_address()`

    This method allows to get a number of street fields according to
    your choice. 2 fields by default in Odoo with 128 width chars.
    In some countries you have constraints on width of street fields and you
    should use 3 or 4 shorter fields.
    You also need of this feature to avoid headache with overflow printing task
