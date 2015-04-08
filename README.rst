Partner Identification Numbers
==============================

This module allows to manage all sort of identification numbers
and certificates which are assigned to a partner and vary from country
to country.

* Commercial register
* VAT ID (eventually)
* Fiscal ID's
* Membership numbers
* Driver license
* ...


Installation
============

Install this addon from Settings > Local Modules, as usual.


Configuration
=============

Configure all ID types you need in Sales > Configuration > Address Book > Partner ID Categories.
For example, we create a category 'Driver License':

* Name : Name of this ID type. For example, 'Driver License'
* Code : Code, abbreviation or acronym of this ID type. For example, 'driver_license'


Usage
=====

In partner form you will see another tab called 'ID Numbers'. You can add
any IDs to this partner, defining:

* Category    : ID type defined in configuration. For example, Driver License
* ID Number   : The ID itself. For example, Driver License number of this person
* Issued by   : Another partner, who issued this ID. For example, Traffic National Institution
* Valid from  : Issued date. For example, date when person approved his driving exam, 21/10/2009
* Valid until : Expiration date. For example, date when person needs to renew his driver license, 21/10/2019
* Notes       : Any further information related with this ID. For example, vehicle types this person can drive


Known issues / Roadmap
======================

If you want to search a partner by ID you will use advance search form.
You can't search by issuer, valid dates, category or notes.


Credits
=======

Contributors
------------
* Antonio Espinosa <antonioea@antiun.com>
