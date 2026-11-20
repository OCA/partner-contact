After installing the module, multi-company users will see a new "Owner Company" field on contact forms.

Child contacts inherit their parent's owner company automatically, including when they are moved to another parent.
The owner company is read-only on child contacts. Change it on the top-level contact instead; changes also apply to archived descendants. Synchronization starts from the top-level contact, so all branches of its contact hierarchy use the same owner company.

Clearing a parent's owner company clears it for its descendants.
Removing a contact's parent keeps its last inherited owner company, which can then be edited independently.

When selecting a contact in a dropdown selection field, partial-name searches propose contacts owned by the current company or global contacts.
If no matching contact is found, contacts owned by other companies can still be selected by an exact match of their name, reference code, email, or Tax/VAT number.

This filtering applies only to the dropdown's autocomplete suggestions (`name_search`).
The **Search More** dialog and the Contacts list do not apply this owner-company filtering: partial-name searches there can return contacts owned by other companies, subject to the usual access rights and record rules.
The owner company is not an access restriction.
