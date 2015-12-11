.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Partner Create by VAT
=====================

This module allows you to create the partners (companies) based on their
VAT number. It will complete the name, address of the partner from
VIES Webservice.

VIES Service (based on stdnum python)
http://ec.europa.eu/taxation_customs/vies/vieshome.do

Installation
============

To install this module, you need to:

* clone the branch 8.0 of the repository https://github.com/OCA/partner-contact
* add the path to this repository in your configuration (addons-path)
* update the module list
* search for "Partner Create by VAT" in your addons
* install the module

Usage
=====

On the partner form view you will have a button in the header, called
"Get Partner Data", available only on companies (is_company field set to True).
Pushing the button will fetch datas from the VIES Webservice, for most of
the countries from EU, the datas are available, only Germany and UK
doesn't provide all the datas.

* Note: When creating a new partner, you can put the VAT number in the name field and the method will get it from there.
      
.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/partner-contact/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/partner-contact/issues/new?body=module:%20partner_create_by_vat%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Fekete Mihai <feketemihai@gmail.com>

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
