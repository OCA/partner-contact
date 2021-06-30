In the old days of Odoo/OpenERP, back in version 6.1, there was an official
*google_map* module ; this module added a *Map* button on the partner form view
and, when the user clicked on that button, it would open a new tab on its web
browser and go to Google Map with a search on the address of the partner.

This module aims at restoring this feature with several improvements:

* Each user can select the map website he wants to use in its preferences.
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

If partner has the latitude and longitude information, Odoo will use that
information instead of the address.
