================================================================================================
Create a Group that can only create and edit Child-Contacts (but not Parent-Top Level Contacts).
================================================================================================

This module allows Fulton to change the default contact creation for new users so they can only create Child-Contacts for Companies.
To create a Top-Level Company, users will have to be part of the Existing Extra Rights/Contact Creation group, 
but not part of Extra Rights/Child Contact Creation Only group.

Since all new users are assigned to this group  by default, Odoo will have to be configured to make the new Extra Rights/Child Contact Group
the default and remove this group from existing users that will not be creating/editing Customer Contacts

============
Installation
============

To install this module, you need to:

 * Go to Settings / Local Modules
 * Search by module name "Partner Contact Creation Security" or
   by module technical name "*partner_contact_creation_security*"
 * Click install button

==============
Configuration
==============
"Create contacts" group is automatically added to new users.Checking Child Contact Creation will limit this user's permissions. 
To maintain all Partner Contact permission, user will only want Contact Creation checked.
Both Extra Rights/Contact Creation and Extra Rights/Child Contact Only Creation" should be the default for new and limited users.
If users will need all Contact Create, Edit, Delete rights, only Contact Creation should be checked. 
The default user is the template used for new users, and is inactive. To access it, we first need to filter the users list by "Active is False".

======
Usage
======
When this module is installed and the above are completed, limited users will only have access to create and update the Child-Contacts 
of Parent Companies. The Extra Rights/ Contact Creation group will be narrowed down to those who need the ability to manage Company contacts.

