[![Runbot Status](https://runbot.odoo-community.org/runbot/badge/flat/134/10.0.svg)](https://runbot.odoo-community.org/runbot/repo/github-com-oca-partner-contact-134)
[![Build Status](https://travis-ci.org/OCA/partner-contact.svg?branch=10.0)](https://travis-ci.org/OCA/partner-contact)
[![Coverage Status](https://coveralls.io/repos/OCA/partner-contact/badge.svg?branch=10.0)](https://coveralls.io/r/OCA/partner-contact?branch=10.0)

OCA partner and contact management modules for Odoo
===================================================

This project is meant to gather all community extensions about partner and contact management for Odoo.

Here you should find community modules that:

* Enable isolated contact management.
* Add first name, birth name, street number and other extensions for the partners.
* Manage cities and post codes.
* Etc.

[//]: # (addons)

Available addons
----------------
addon | version | summary
--- | --- | ---
[base_country_state_translatable](base_country_state_translatable/) | 10.0.1.0.0 | Translate Country States
[base_location](base_location/) | 10.0.1.0.1 | Enhanced zip/npa management system
[base_location_geonames_import](base_location_geonames_import/) | 10.0.1.1.1 | Import better zip entries from Geonames
[base_location_nuts](base_location_nuts/) | 10.0.1.0.0 | NUTS Regions
[base_partner_merge](base_partner_merge/) | 10.0.1.0.0 | Partner merge wizard without dependency on CRM
[base_partner_sequence](base_partner_sequence/) | 10.0.1.0.0 | Sets customer's code from a sequence
[base_vat_sanitized](base_vat_sanitized/) | 10.0.1.0.0 | Adds field sanitized_vat on partners
[partner_academic_title](partner_academic_title/) | 10.0.1.0.0 | Add possibility to define some academic title
[partner_address_street3](partner_address_street3/) | 10.0.1.0.0 | Add a third address line on partners
[partner_affiliate](partner_affiliate/) | 10.0.1.0.0 | Partner Affiliates
[partner_alias](partner_alias/) | 10.0.1.0.0 | Adds aliases to partner names.
[partner_bank_active](partner_bank_active/) | 10.0.1.0.0 | Allow to deactivate a partner bank account
[partner_capital](partner_capital/) | 10.0.1.0.0 | Partners Capital
[partner_changeset](partner_changeset/) | 10.0.1.0.1 | Partner Changesets
[partner_coc](partner_coc/) | 10.0.1.0.0 | Adds a field 'Chamber Of Commerce Registration Number' to partner
[partner_company_type](partner_company_type/) | 10.0.1.0.1 | Adds a company type to partner that are companies
[partner_contact_birthdate](partner_contact_birthdate/) | 10.0.1.1.0 | Contact's birthdate
[partner_contact_configuration](partner_contact_configuration/) | 10.0.1.0.0 | Adds menu configuration access through the 'contacts' module main menu
[partner_contact_department](partner_contact_department/) | 10.0.1.0.0 | Assign contacts to departments
[partner_contact_gender](partner_contact_gender/) | 10.0.1.1.0 | Add gender field to contacts
[partner_contact_in_several_companies](partner_contact_in_several_companies/) | 10.0.1.0.0 | Allow to have one contact in several partners
[partner_contact_job_position](partner_contact_job_position/) | 10.0.1.0.1 | Categorize job positions for contacts
[partner_contact_lang](partner_contact_lang/) | 10.0.1.0.0 | Manage language in contacts
[partner_contact_nationality](partner_contact_nationality/) | 10.0.1.0.0 | Add nationality field to contacts
[partner_contact_nutrition](partner_contact_nutrition/) | 10.0.1.0.0 | Provide caloric intake
[partner_contact_nutrition_activity_level](partner_contact_nutrition_activity_level/) | 10.0.1.0.0 | Set the activity level of your contacts
[partner_contact_nutrition_goal](partner_contact_nutrition_goal/) | 10.0.1.0.0 | Set the nutrition goal of your contacts
[partner_contact_personal_information_page](partner_contact_personal_information_page/) | 10.0.1.0.0 | Add a page to contacts form to put personal information
[partner_contact_weight](partner_contact_weight/) | 10.0.1.0.0 | Provide contact weight
[partner_create_by_vat](partner_create_by_vat/) | 10.0.1.0.0 | Using VIES webservice, name and address information will be fetched and added to the partner.
[partner_email_check](partner_email_check/) | 10.0.1.0.0 | Validate email address field
[partner_employee_quantity](partner_employee_quantity/) | 10.0.1.0.0 | Know how many employees a partner has
[partner_external_map](partner_external_map/) | 10.0.1.0.0 | Add Map and Map Routing buttons on partner form to open GMaps, OSM, Bing and others
[partner_firstname](partner_firstname/) | 10.0.2.1.1 | Split first name and last name for non company partners
[partner_helper](partner_helper/) | 10.0.0.1.0 | Add specific helper methods
[partner_identification](partner_identification/) | 10.0.1.1.1 | Partner Identification Numbers
[partner_label](partner_label/) | 10.0.1.0.0 | Print partner labels
[partner_multi_relation](partner_multi_relation/) | 10.0.1.0.1 | Partner relations
[partner_password_reset](partner_password_reset/) | 10.0.1.0.0 | Add Wizard to allow resetting of a Partner's associated user password from within the partner view.
[partner_phone_extension](partner_phone_extension/) | 10.0.1.0.0 | Partner Phone Number Extension
[partner_phonecall_schedule](partner_phonecall_schedule/) | 10.0.1.0.0 | Track the time and days your partners expect phone calls
[partner_second_lastname](partner_second_lastname/) | 10.0.1.0.0 | Have split first and second lastnames
[partner_sector](partner_sector/) | 10.0.1.0.0 | Add partner sectors
[partner_street_number](partner_street_number/) | 10.0.1.0.0 | Introduces separate fields for street name and street number.


Unported addons
---------------
addon | version | summary
--- | --- | ---
[account_partner_merge](account_partner_merge/) | 1.0 (unported) | Account Partner Merge
[base_continent](base_continent/) | 8.0.1.0.0 (unported) | Continent management
[firstname_display_name_trigger](firstname_display_name_trigger/) | 1.0 (unported) | Link module if partner_lastname and account_report_company are installed
[partner_auto_salesman](partner_auto_salesman/) | 8.0.1.0.0 (unported) | Partner auto salesman
[partner_contact_address_detailed](partner_contact_address_detailed/) | 8.0.1.0.0 (unported) | All address data in summarized contact form
[portal_partner_merge](portal_partner_merge/) | 8.0.1.0.0 (unported) | Portal Partner Merge

[//]: # (end addons)

Translation Status
------------------
[![Transifex Status](https://www.transifex.com/projects/p/OCA-partner-contact-10-0/chart/image_png)](https://www.transifex.com/projects/p/OCA-partner-contact-10-0)

----

OCA, or the Odoo Community Association, is a nonprofit organization whose 
mission is to support the collaborative development of Odoo features and 
promote its widespread use.

http://odoo-community.org/
