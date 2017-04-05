.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Partner Helper
==============

The purpose of this module is to gather generic partner methods.
It avoids to grow up excessively the number of modules in Odoo
for small features.

Description
-----------
Add specific helper methods to deal with partners:

* _get_split_address():
    This method allows to get a number of street fields according to
    your choice. 2 fields by default in Odoo with 128 width chars.
    In some countries you have constraints on width of street fields and you
    should use 3 or 4 shorter fields.
    You also need of this feature to avoid headache with overflow printing task

* other_method():



Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/partner_contact/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.


Contributors
------------

 * Sébastien BEAU <sebastien.beau@akretion.com>
 * David BEAL <david.beal@akretion.com>


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
