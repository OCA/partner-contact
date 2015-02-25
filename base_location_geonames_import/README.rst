Base Location Geonames Import
=============================

This module adds a wizard to import better zip entries from Geonames database.

Installation
============
For installing this module, you need these Python libraries: requests and
unicodecsv.

Configuration
=============

For seeing the menu, you need to activate *Technical features* option in your 
user and to be *Sales manager*.

If want want/need to modify the default URL
(http://download.geonames.org/export/zip/), you can set the 'geonames.url'
system parameter.

Usage
=====

Go to *Sales > Configuration > Address book > Localization > Import from Geonames*,
and click on it to open a wizard.

When you start the wizard, it will ask you to select a country. Then, for the
selected country, it will delete all the current better zip entries, download
the latest version of the list of cities from geonames.org and create new
better zip entries.

Credits
=======

Contributors
------------

* Alexis de Lattre <alexis.delattre@akretion.com>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>

Icon
----
* http://icon-park.com/icon/location-map-pin-orange3/
* http://commons.wikimedia.org/wiki/File:View-refresh.svg


Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
