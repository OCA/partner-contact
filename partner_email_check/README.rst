.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================
Partner Email Check
===================

This module validates and normalizes the field ``email`` in the model
``res.partner``.

As part of the normalization, email addresses are converted to lowercase.

Optionally, multiple partners can not be allowed to have the same address.
This will not work with multiple comma-separated email addresses in the field,
although validation and normalization are still supported in such cases.

Configuration
=============

Install python package email-validator: ``sudo pip install email-validator``.

To not allow multiple partners to have the same email address, use the
"Filter duplicate email addresses"/``partner_email_check_filter_duplicates``
setting.

To validate that email addresses are deliverable (that the hostname exists),
use the "Check deliverability of email addresses"/``partner_email_check_check_deliverability``
setting.

Usage
=====

This module integrate automatically in all of the view ``res.partner``

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/partner-contact/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Vo Hoang Dat <dat.vh@komit-consulting.com>
* Jean-Charles Drubay <jc@komit-consulting.com>

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
