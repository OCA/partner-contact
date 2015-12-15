.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==========================
NACE Activities in Partner
==========================

This module adds the concept of NACE activity to the partner.

NACE is the Statistical Classification of Economic Activities in the European
Community. More info at http://ec.europa.eu/eurostat/en/web/products-manuals-and-guidelines/-/KS-RA-07-015

Allows you to select in partner form:

* Main NACE activity in a dropdown (many2one)
* Secondary NACE activities in a multi label input (many2many)

This addon is inspired in OCA/community-data-files/l10n_eu_nace, but it does
not use partner categories to assign NACE activities to partner.

Installation
============

To install this module, you need request python module:

* pip intall requests

Configuration
=============

After installation, you must click at import wizard to populate NACE items
in Odoo database in:
Sales > Configuration > Address Book > Import NACE Rev.2 from RAMON

This wizard will download from Europe RAMON service the metadata to
build NACE database in Odoo in all installed languages.

If you add a new language (or want to re-build NACE database), you should call
import wizard again.

Usage
=====

Only Administrator can manage NACE activity list (it is not neccesary because
it is an European convention) but any registered user can read them,
in order to allow to assign them to partner object.

After configuration, all NACE activities are available to be selected in
partner form as main and secondary activities.

Applies only to partners marked as companies

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/8.0


For further information, please visit:

* https://www.odoo.com/forum/help-1

Known issues / Roadmap
======================

* Improve import algorithm: Use context lang key to translate NACE items


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/partner-contact/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/partner-contact/issues/new?body=module:%20partner_nace%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Rafael Blasco <rafabn@antiun.com>
* Antonio Espinosa <antonioea@antiun.com>
* Javier Iniesta <javieria@antiun.com>

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
