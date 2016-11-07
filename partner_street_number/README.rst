.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Split street name and number
============================

This module introduces separate fields for street name and street number.

Changes to the Odoo datamodel
=============================
- Introduce two new fields for street name and number
- Keep 'Street' field as a function field to return street name + number
- Data written to the 'Street' field will be parsed into street name and number
  if possible. This will be performed upon installation of the module for
  existing partners.

Compatibility
=============
This module is compatible with Odoo 10.0.


Installation
============

Upon installation, the module will do a simple migration of existing values in
the street column to split up the street name and number.

Usage
=====

To use this module, you need to:

#. Open a partner form
#. Fill fields street name and number

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/10.0

Known issues / Roadmap
======================

* Add more unit tests

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

* Stefan Rijnhart <stefan@therp.nl>
* Ronald Portier <ronald@therp.nl>
* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
* Andrea Stirpe <a.stirpe@onestein.nl>

Icon
----

* Based on https://openclipart.org/detail/149575/brass-plaques-tags.

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
