This module allows you to create the partners (companies) based on their VAT number.
Name and address of the partner will automatically be completed via VIES Webservice.

VIES Service (based on stdnum python)
https://ec.europa.eu/taxation_customs/vies/#/vat-validation

Unfortunately, VIES doesn't return a structured address but just a one-line address that aggregate street, zip and city. So, when you use this module to create a partner, the *City* and *Zip* fields will be left empty ; the *Street* field will contain the one-line address.
