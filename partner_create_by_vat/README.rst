.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

==============================================
Automatic partner creation based on VAT number
==============================================

This module allows you to create the partners (companies) based on their VAT number.
Name and address of the partner will automatically be completed via VIES Webservice.

VIES Service (based on stdnum python)
http://ec.europa.eu/taxation_customs/vies/vieshome.do

Installation
============

To install this module, you need to:

#. Clone the branch 10.0 of the repository https://github.com/OCA/partner-contact
#. Add the path to this repository in your configuration (addons-path)
#. Update the module list
#. Search for "Partner Create by VAT" in your addons
#. install the module

Usage
=====

On the partner's form view you will have a button in the header, called
"Get Vies Data", available only on companies (is_company field set to True).
Clicking the button will fetch data, when available, from the VIES Webservice, for most of
the EU countries.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/10.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/partner-contact/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Fekete Mihai <feketemihai@gmail.com>

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
