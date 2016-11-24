.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Manage language in contacts
===========================

Odoo by default propagate language field to the created contacts from their
form, but it doesn't allow to change it once created.

This module fills this gap, and also provides other facilities for the
contact language management:

* Put the language of the parent company when the contact doesn't have a
  language and this parent company is assigned.
* When the company changes the language, it fills with the same language all
  the contacts that don't have any.

Usage
=====

Go to any partner that is a company and has contacts. Click on one contact
and you will be able to edit the language.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/partner-contact/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Pedro M. Baeza <pedro.baeza@tecnativa.com>

Icon
----
* Original Odoo icons.

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
