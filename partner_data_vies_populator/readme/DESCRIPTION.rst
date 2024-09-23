This module allows you to create the partners (companies) based on their VAT number.
Name and address of the partner will automatically be completed via VIES Webservice.

VIES Service (based on stdnum python)
http://ec.europa.eu/taxation_customs/vies

Unfortunately, VIES doesn't return a structured address but just a multi-line string
with aggregate street, zip and city.

So, when the data is retrieved, it will try to populate the *City* and *Zip* fields
from the last line of the address.
T he *Street* field will contain the remaining information.
