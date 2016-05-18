.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==========================
Local Administrative Units
==========================

Add support to local administrative areas, such as municipalities.
Two new fields are added to the Partners model: LAU1 and LAU2.

It is compatible with the Eurostat NUTS\LAU structure.
* The upper LAU level (LAU level 1, formerly NUTS level 4) is defined for most,
  but not all of the countries.
* The lower LAU level (LAU level 2, formerly NUTS level 5) consists of
  municipalities or equivalent units in the 28 EU Member States.

Se also: http://ec.europa.eu/eurostat/web/nuts/local-administrative-units


Installation
============

No data is provided by this module.
Country specific data should be provided by localization modules.


Configuration
=============

The Local Administrative Units table setup can be done under
Sales > Configuration > Address Book


Usage
=====


Only Administrator can manage LAUs, but any registered user can read them,
in order to allow to assign them to Partners.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/partner-contact/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/partner-contact/issues/new?body=module:%20base_location_lau%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Roadmap / Known Issues
======================

* The LAU fields are not added to the Partner form.
* LAU fields could also be added to Employees, to allow meeting
  local reporting requirements.


Credits
=======

Contributors
------------

* Daniel Reis <dreis.pt(at)hotmail.com>

Based on the base_location_nuts module contributed by:

* Rafael Blasco <rafabn@antiun.com>
* Antonio Espinosa <antonioea@antiun.com>
* Jairo Llopis <yajo.sk8@gmail.com>


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
