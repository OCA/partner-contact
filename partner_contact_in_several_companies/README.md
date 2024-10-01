# Partner Contact in Several Companies

This module extends Odoo's Contacts app to **allow one contact to have several job
positions in different companies**. It is an essential add-on for handling the 'gig
economy' where people often work for several companies at a time (e.g., film and
television industry, contract developers, construction, etc.)

Contacts are categorized as either:

- **Standalone Contact** (default): A normal contact (either an Individual or a
  Company), though only Individual Standalone contacts can be linked to.
- **Attached to existing Contact**: Usually used when adding a contact under a Company,
  this contact is linked to a source Standalone Contact. Source contacts can only be
  Individuals, not Companies, nor can an Attached contact serve as the source of another
  Attached contact.

## Installation

1. Download the module from the OCA repository (ensure any dependencies are satisfied).
2. Place the module in your Odoo addons directory.
3. Restart the Odoo service.
4. In Odoo, go to Apps > Update Apps List.
5. Find and install the Partner Contact in Several Companies module.

After installation, all existing contacts will be of type Standalone (the default for
the field contact_type).

## Configuration

No configuration is needed: new contacts will automatically be of type Standalone.

## Usage

To add a new Standalone contact, add a contact as usual, either by itself or under an
existing contact's Contacts & Addresses tab (the Contact Type will be 'Standalone' by
default). Any Standalone Individual contact can serve as the source for Attached
contacts, whether that Standalone contact was added by itself or under an existing
Company's or Individual's Contacts & Addresses tab.

### To add a new Attached contact:

1. Ensure that the source Standalone contact is already created, though you can create
   the Standalone contact on-the-fly if needed.
2. Open the contact under which you would like to add the Attached contact (usually a
   Company, but it could be an Individual).
3. On the Contacts & Addresses tab, click the Add button.
4. Choose the type of contact you are adding (e.g. Contact, Delivery Address, Other
   Address, etc., though usually you will select Contact).
5. Select 'Attached to existing Contact' for the Contact Type
6. Select the source Standalone contact in the Contact drop-down list (or create a new
   one on-the-fly). Only contacts that are Standalone and are Individuals will appear in
   the list.
7. Fill in the other informational fields (e.g. Address, Email, Phone, etc.) This data
   will not be copied or synchronized from the source Standalone contact.
8. Click the Save & Close button (or Save & New). The Attached contact will appear in
   the Contacts & Addresses tab of the parent Company, and in the Other Positions tab of
   the source Standalone contact.
9. If you later change the Name of either a Standalone or Attached contact, the Name
   will be synchronized between all related contacts. However, other information (e.g.,
   Address, Email, Phone, etc.) will not be synchronized.

### Searching for Contacts:

When searching for Contacts, only the matching Standalone contacts are displayed, with
the number of Attached contacts shown as '+ # other position(s)'. Open the Standalone
contact and select the Other Positions tab to see the contacts that are 'Attached' to
this Standalone contact.

### NOTES:

1. This module merely sets up a relationship between the Standalone and Attached
   contacts — other than 'Name', there is no address, phone, email, etc. information
   synchronized or carried-over from one to the other. For example, an email address in
   the Standalone contact is not carried over to the Attached contact when created (and
   indeed they can both have different email addresses). The contact Name is however
   synchronized between Standalone and associated Attached contacts.
2. Attached contacts are not treated as duplicates when performing the Contact Merge
   action due to Attached contacts being specifically removed from the results of the
   res_partner.search() method (i.e. only Standalone contacts are returned during a
   res_partner.search()).
3. This module is compatible with the OCA's Partner Contact Access Link
   (partner_contact_access_link) module.
4. When you install this module, existing contacts will all become Standalone contacts.
   If there are any child contacts of Companies that you would like to convert to
   Attached to an existing contact, it is a manual process: create the new Standalone
   contact without any parent, and then change the child contact's Contact Type from
   'Standalone' to 'Attached to existing Contact' and choose the new Standalone contact
   that you created without any parent.
