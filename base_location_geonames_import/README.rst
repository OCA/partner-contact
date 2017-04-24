.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================
Base Location Geonames Import
=============================

This module adds a wizard to import better zip entries from `Geonames <http://www.geonames.org/>`_ database.

Installation
============

To install this module, you need these Python libraries: requests and
unicodecsv.

Configuration
=============

To access the menu to import better zip entries from Geonames, you must add yourself to the groups *Technical features* and *Sales manager*.

If want want/need to modify the default URL
(http://download.geonames.org/export/zip/), you can set the *geonames.url*
system parameter.

Usage
=====

Go to *Settings > Technical > Cities/Locations Management > Import from Geonames*,
and click on it to open a wizard.

When you start the wizard, it will ask you to select a country. Then, for the
selected country, it will delete all the current better zip entries, download
the latest version of the list of cities from geonames.org and create new
better zip entries.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/10.0

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

* Alexis de Lattre <alexis.delattre@akretion.com>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
* Dave Lasley <dave@laslabs.com>

Icon
----

* http://icon-park.com/icon/location-map-pin-orange3/
* http://commons.wikimedia.org/wiki/File:View-refresh.svg

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
