.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

======================================
Add a sequence on partner's reference.
======================================

This module adds the possibility to define a sequence for
the partner's reference. This reference is then set as default 
when you create a new partner, using the defined sequence.

The reference field is treated as a commercial field, i.e. it
is managed from the commercial partner and then propagated to
the partner's contacts. The field is visible on the contacts,
but it can only be modified from the commercial partner.

No references are assigned for contacts such as shipping and
invoice addresses.
This module is a migration of the original base_partner_sequence
addon to OpenERP version 7.0.


Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/8.0


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/partner-contact/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/partner-contact/issues/new?body=module:%base_partner_sequence%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Thomas Rehn <thomas.rehn@initos.com>
* Stefan Rijnhart <stefan@therp.nl>
* Yannick Vaucher <yannick.vaucher@camptocamp.com>
* Sandy Carter <sandy.carter@savoirfairelinux.com>
* Laurent Mignon (ACSONE) <laurent.mignon@acsone.eu>
* Guewen Baconnier <guewen.baconnier@camptocamp.com>
* Alexandre Fayolle <alexandre.fayolle@camptocamp.com>

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
