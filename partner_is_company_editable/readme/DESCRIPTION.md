In Odoo 20, you cannot choose if a contact is a company or a person.
Odoo decides it from the Tax ID:

- with a Tax ID, the contact is a company;
- without a Tax ID, the contact is a person.

Some countries add their own rule. For example, in Thailand only a Tax ID
that starts with "0" means a company.

This rule is not always right, for example for a company that has no Tax ID
yet. This module adds back the *Is a Company* checkbox on the contact form,
so you can fix it by hand.
