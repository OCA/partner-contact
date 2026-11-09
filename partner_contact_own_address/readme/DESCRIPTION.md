In Odoo, a contact of type "Contact" shares the address of its parent
company. Editing the address on the contact changes the company address, and
editing the company address changes the address of all its contacts.

This module adds an "Own Address" option on contacts. A contact with this
option keeps its own address, for example a person working from home, while it
stays a contact of the company:

- Editing the contact address does not change the company address.
- Editing the company address does not change the contact address.
- Moving the contact to another company keeps its address.
