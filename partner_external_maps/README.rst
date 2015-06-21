Partner External Maps
=====================

In the old days of Odoo/OpenERP, back in version 6.1, there was an official *google_map* module ; this module added a *Map* button on the partner form view and, when the user clicked on that button, it would open a new tab on its web browser and go to Google Map with a search on the address of the partner.

This module aims at restoring this feature with several improvements:

* each user can select the map website he wants to use in its preferences

* there are now two buttons on the partner form view: one to open a regular map on the address of the partner, and another one to open an itinerary map from the start address configured in the preferences of the user to the address of the partner.

This module supports several map websites:

* `Google Maps <https://www.google.com/maps>`

* `OpenStreetMap <https://www.openstreetmap.org/>`

* `Bing Maps <https://www.bing.com/maps/>`

* `Here Maps <https://www.here.com/>`

* `MapQuest <http://www.mapquest.com/>`

* `Yahoo! Maps <https://maps.yahoo.com/>`

If the module *base_geolocalize* from the official addons is installed on the system, it will use the latitude and longitude to localize the partner (instead of the address) if this information is present on the partner.

Configuration
=============

If you want to create additionnal map websites, go to the menu *Sales > Configuration > Address Book > Localization > Map Websites*. You are invited to send the configuration information of your additionnal map websites to the author of the module, so that the module can be updated with more pre-configured map websites.

Usage
=====

First, you need to configure in your preferences:

* the map website to use for the regular maps,

* the map website to use for the route maps,

* the start address for the route maps.

Then you can use the two new buttons on the partner form to open a regular map or a route map.

Credits
=======

Contributors
------------

* Alexis de Lattre <alexis.delattre@akretion.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
