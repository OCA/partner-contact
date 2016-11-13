.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

================================
Partner first name and last name
================================

This module was written to extend the functionality of contacts to support
having separate last name and first name.

Configuration
=============

You can configure some common name patterns for the inverse function
in Settings > Configuration > General settings:

* Lastname Firstname: For example 'Anderson Robert'
* Lastname, Firstname: For example 'Anderson, Robert'
* Firstname Lastname: For example 'Robert Anderson'

After applying the changes, you can recalculate all partners name clicking
"Recalculate names" button. Note: This process could take so much time depending
how many partners there are in database.

You can use *_get_inverse_name* method to get lastname and firstname from a simple string
and also *_get_computed_name* to get a name form the lastname and firstname.
These methods can be overridden to change the format specified above.


Usage
=====

The field *name* becomes a stored function field concatenating the *last name*
and the *first name*. This avoids breaking compatibility with other modules.

Users should fulfill manually the separate fields for *last name* and *first
name*, but in case you edit just the *name* field in some unexpected module,
there is an inverse function that tries to split that automatically. It assumes
that you write the *name* in format configured (*"Lastname Firstname"*, by default),
but it could lead to wrong splitting (because it's just blindly trying to
guess what you meant), so you better specify it manually.

For the same reason, after installing, previous names for contacts will stay in
the *name* field, and the first time you edit any of them you will be asked to
supply the *last name* and *first name* (just once per contact).

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/10.0

For further information, please visit:

* https://www.odoo.com/forum/help-1


Known issues / Roadmap
======================

Patterns for the inverse function are configurable only at system level. Maybe
this configuration could depend on partner language, country or company,
as discussed at `this OCA issue <https://github.com/OCA/partner-contact/issues/210>`_


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

* Nicolas Bessi <nicolas.bessi@camptocamp.com>
* Yannick Vaucher <yannick.vaucher@camptocamp.com>
* Vincent Renaville <vincent.renaville@camptocamp.com>
* Guewen Baconnier <guewen.baconnier@camptocamp.com>
* Holger Brunn <hbrunn@terp.nl>
* Jonathan Nemry <jonathan.nemry@acsone.eu>
* Olivier Laurent <olivier.laurent@acsone.eu>
* Sandy Carter <sandy.carter@savoirfairelinux.com>
* Alexis de Lattre <alexis.delattre@akretion.fr>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Hans Henrik Gabelgaard <hhg@gabelgaard.org>
* Jairo Llopis <j.llopis@grupoesoc.es>
* Adrien Peiffer <adrien.peiffer@acsone.eu>
* Ronald Portier <ronald@therp.nl>
* Sylvain Van Hoof
* Pedro Baeza <pedro.baeza@serviciosbaeza.com>
* Dave Lasley <dave@laslabs.com>

Translations
------------

* Danish: Hans Henrik Gabelgaard
* Italian: Leonardo Donelli
* Spanish: Antonio Espinosa
* Antonio Espinosa <antonioea@antiun.com>

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
