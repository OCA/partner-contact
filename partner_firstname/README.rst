.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Partner first name and last name
================================

This module was written to extend the functionality of contacts to support
having separate last name and first name.

Usage
=====

The field *name* becomes a stored function field concatenating the *last name*
and the *first name*. This avoids breaking compatibility with other modules.

Users should fulfill manually the separate fields for *last name* and *first
name*, but in case you edit just the *name* field in some unexpected module,
there is an inverse function that tries to split that automatically. It assumes
that you write the *name* in format *"Lastname Firstname"*, but it could lead to
wrong splitting (because it's just blindly trying to guess what you meant), so
you better specify it manually.

For the same reason, after installing, previous names for contacts will stay in
the *name* field, and the first time you edit any of them you will be asked to
supply the *last name* and *first name* (just once per contact).

You can use *_get_inverse_name* method to get lastname and firstname from a simple string
and also *_get_computed_name* to get a name form the lastname and firstname. 
These methods can be overridden to change the format specified above

For further information, please visit:

* https://www.odoo.com/forum/help-1

Credits
=======

Contributors
------------

* Nicolas Bessi <nicolas.bessi@camptocamp.com>
* Jonathan Nemry <jonathan.nemry@acsone.eu>
* Olivier Laurent <olivier.laurent@acsone.eu>
* Hans Henrik Gabelgaard <hhg@gabelgaard.org>
* Jairo Llopis <j.llopis@grupoesoc.es>
* Adrien Peiffer <adrien.peiffer@acsone.eu>

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
