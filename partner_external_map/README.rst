.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================
Partner External Maps
=====================

In the old days of Odoo/OpenERP, back in version 6.1, there was an official
*google_map* module ; this module added a *Map* button on the partner form view
and, when the user clicked on that button, it would open a new tab on its web
browser and go to Google Map with a search on the address of the partner.

This module aims at restoring this feature with several improvements:

* Each user can select the map website he wants to use in its preferences
* There are now two buttons on the partner form view: one to open a regular map
  on the address of the partner, and another one to open an itinerary map from
  the start address configured in the preferences of the user to the address of
  the partner.

This module supports several map websites:

* `Google Maps <https://www.google.com/maps>`
* `OpenStreetMap <https://www.openstreetmap.org/>`
* `Bing Maps <https://www.bing.com/maps/>`
* `Here Maps <https://www.here.com/>`
* `MapQuest <http://www.mapquest.com/>`
* `Yahoo! Maps <https://maps.yahoo.com/>`

If the module *base_geolocalize* from the official addons is installed on the
system, it will use the latitude and longitude to localize the partner (instead
of the address) if this information is present on the partner.

Configuration
=============

If you want to create additionnal map websites, go to the menu
*Sales > Configuration > Address Book > Localization > Map Websites*. You are
invited to send the configuration information of your additionnal map websites
to the author of the module, so that the module can be updated with more
pre-configured map websites.

Usage
=====

First, you need to configure in your preferences:

* The map website to use for the regular maps,
* The map website to use for the route maps,
* The start address for the route maps.

Then you can use the two new buttons on the partner form to open a regular map
or a route map.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/9.0

Known issues / Roadmap
======================

* Let decide if the user prefers to use addresses instead coordinates when
  *base_geolocalize* is installed.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/partner-contact/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
partner-contact/issues/new?body=module:%20
partner_external_map%0Aversion:%20
9.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Alexis de Lattre <alexis.delattre@akretion.com>
* Pedro M. Baeza <pedro.baeza@tecnativa.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
