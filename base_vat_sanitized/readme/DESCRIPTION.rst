**THIS MODULE WAS PORTED TO ODOO 13.0 BY MISTAKE: DON'T INSTALL IT**. The feature is now native in Odoo 13.0 (it is implemented in the `base_vat <https://github.com/odoo/odoo/tree/13.0/addons/base_vat>`_ module).

This module adds a technical field *sanitized_vat* on partners that stores the VAT number
without spaces and with letters in uppercase. It is useful for other modules that need to
match partners on VAT number, such as the *base_business_document_import* module for example.
