.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================
Partner Identification Numbers
==============================

This module allows to manage all sort of identification numbers
and certificates which are assigned to a partner (company or individual)
and vary from country to country.

* Commercial register
* VAT ID
* Fiscal ID's
* Membership numbers
* Driver license
* ...


Installation
============

No specific installation step required


Configuration
=============

Configure all ID types you need in Sales > Configuration > Address Book > Partner ID Categories.
For example, we create a category 'Driver License':

Name:
  Name of this ID type. For example, 'Driver License'
Code:
  Code, abbreviation or acronym of this ID type. For example, 'driver_license'
Python validation code:
  Optional python code called to validate ID numbers of this ID type.


Usage
=====

In partner form you will see another tab called 'ID Numbers'. You can add
any IDs to this partner, defining:

Category:
   ID type defined in configuration. For example, Driver License
ID Number:
  The ID itself. For example, Driver License number of this person
Issued by:
  Another partner, who issued this ID. For example, Traffic National Institution
Place of Issuance:
  The place where the ID has been issued. For example the country for passports and visa
Valid from:
  Issued date. For example, date when person approved his driving exam, 21/10/2009
Valid until:
  Expiration date. For example, date when person needs to renew his driver license, 21/10/2019
Status:
  ID status. For example new/to renew/expired
Notes:
  Any further information related with this ID. For example, vehicle types this person can drive

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/


Known issues / Roadmap
======================

* If you want to search a partner by ID you will use advance search form.
  You can't search by issuer, valid dates, category or notes.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/partner_contact/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
partner_contact/issues/new?body=module:%20
partner_identifiers%0Aversion:%20
9.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Antonio Espinosa <antonioea@antiun.com>
* Denis Roussel <denis.roussel@acsone.eu>
* Ferdinand Gassauer <office@chrcar.at>
* Gerhard Könighofer <gerhard.koenighofer@swing-system.com>
* Laurent Mignon <laurent.mignon@acsone.eu>
* Yajo <Yajo@users.noreply.github.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
