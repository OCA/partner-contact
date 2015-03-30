.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

============
NUTS Regions
============

This module allows to import NUTS locations.

Creates two new fields in Partner object:

* Region (res.partner.region): Classification over state, automatically
  calculated when state is selected
* Substate (res.partner.substate): Classification above state, user must select
  one from available for selected state


Installation
============

You need to install another addon (one for each country) in order to use
these NUTS, for example:

* l10n_es_location_nuts :
    * Spanish Provinces (NUTS level 4) as Partner State
    * Spanish Autonomous communities (NUTS level 3) as Partner Substate
    * Spanish Regions (NUTS level 2) as Partner Region
* l10n_de_location_nuts :
    * German states (NUTS level 2) as Partner State
    * German districts (NUTS level 3) as Partner Substate
    * German regions (NUTS level 4) as Partner Region


Configuration
=============

After installation, you must click at import wizard to populate NUTS items
in Odoo database in:
Sales > Configuration > Address Book > Import NUTS 2013

This wizard will download from Europe RAMON service the metadata to
build NUTS in Odoo. Each localization addon (l10n_es_location_nuts,
l10n_de_location_nuts, ...) will inherit this wizard and
relate each NUTS item with states. So if you install a new localization addon
you must re-build NUTS clicking this wizard again.


Usage
=====

Only Administrator can manage NUTS list (it is not neccesary because
it is an European convention) but any registered user can read them,
in order to allow to assign them to partner object.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/{branch}


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/partner-contact/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/partner-contact/issues/new?body=module:%20base_location_nuts%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Rafael Blasco <rafabn@antiun.com>
* Antonio Espinosa <antonioea@antiun.com>

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