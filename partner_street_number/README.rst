.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

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
This module is compatible with OpenERP 8.0.


Installation
============

Upon installation, the module will do a simple migration of existing values in
the street column to split up the street name and number.

Credits
=======

Contributors
------------

* Stefan Rijnhart <stefan@therp.nl>
* Ronald Portier <ronald@therp.nl>
* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>

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
