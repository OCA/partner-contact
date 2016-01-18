.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Module name
===========

This module was written to extend the functionality of Odoo to support setting
a birthdate using a date format and allow you to benefit of a clearer API and
UI.

Installation
============

To install this module, you need to:

* Ensure that the current contents of the *birthdate* field in the
  *res.partner* model in your database are empty or in a format easily readable
  by the python function strptime_ in case you want this module to
  automatically convert those to the new format.
* Install the OCA repository `partner-contact`_.
* Update your modules list.
* Search and install this module.

Configuration
=============

No configuration is needed.

Usage
=====

To use this module, you need to:

* Edit or create a partner.
* Ensure it is **not** a company.
* Go to the *Personal Information* sheet.
* Set the birthdate there.

For further information, please visit:

* https://www.odoo.com/forum/help-1
* https://github.com/OCA/partner-contact/

Known issues / Roadmap
======================

* If you have data in your *res.partner* records' *birthdate* field that cannot
  be converted to date by Pyhton's strptime_ function, those records will have
  an empty *birthdate_date* after install.

Credits
=======

Contributors
------------

* EL Hadji DEM <elhadji.dem@savoirfairelinux.com>
* Jairo Llopis <j.llopis@grupoesoc.es>
* Matjaž Mozetič <m.mozetic@matmoz.si>
* Rudolf Schnapka <schnapkar@golive-saar.de>
* Denis Leemann <denis.leemann@camptocamp.com>

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


.. _partner-contact: https://github.com/OCA/partner-contact/
.. _strptime: https://docs.python.org/2/library/datetime.html#datetime.datetime.strptime
