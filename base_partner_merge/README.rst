.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Deduplicate contacts OCA
========================

This module installs the deduplicate wizard from Odoo CRM, but without the
dependency on the CRM module and with some extra features.

The extra features are:

- Can be installed with or without the CRM module
- Deduplicate also on `ref` (partner reference)
- To deduplicate only a subset of partners (eg. one category), the context
  variable `extra_domain` may contain a domain string to search on before
  deduplicating. (TODO: offer this in the wizard)
- A function `deduplicate_on_field(self, field, domain=[]):` is added to the
  `res.partner` object. It takes the field to deduplicate on as a parameter,
  as well as the domain mentioned above. It can be called from `ir.cron`
  Automated Actions.

Installation
============

To install this module, you need to have `crm` module present on the system.
This is because we reuse the existing code from Odoo CRM.


Known issues
============

If this module is installed, `crm` module installation gives an error.
Workaround for this is to remove this module, install `crm`, then install
this module again.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/partner-contact/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/partner-contact/issues/new?body=module:%20base_partner_merge%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Charbel Jacquin <charbel.jacquin@camptocamp.com>
* Holger Brunn <hbrunn@therp.nl>
* Tom Blauwendraat <tom@sunflowerweb.nl>
* Terrence Nzaywa  <terrence@sunflowerweb.nl>

Author
------

Yannick Vaucher
Based on Holger Brunn's idea
Backported to 8.0 by Tom Blauwendraat and Terrence Nzaywa
Features added by Tom Blauwendraat

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
