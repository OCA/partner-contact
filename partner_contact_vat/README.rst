.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================
VAT in contact partners
=======================

This module was written to extend the functionality of contacts management to
support setting a VAT in contact partners (those partners that are not not
companies) and allow you to have separate VAT codes for contact and for their
company.

Odoo by default only allows VAT in companies. When a contact belongs to a
company and you go to *accounting* page, it shows *Accounting is managed in the
parent company*.

If you manage any kind of personal information of your clients (prevention of
occupational hazards, training, event assistants, legal stuff, etc.) you
probably need their VAT.

Indeed the company VAT will still be used for invoices and other legal
documents, but for other things you need the person's. For that reason, instead
of overwriting the VAT field, this module just adds a new one that will be
hidden for companies.

You will not be able to save a contact VAT with an invalid format.

Usage
=====

To use this module, you need to:

* Go to any contact's form.
* Enter its *personal information* page.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/
partner-contact/issues>`_. In case of trouble, please check there if your issue
has already been reported. If you spotted it first, help us smashing it by
providing a detailed and welcomed feedback `here <https://github.com/OCA/
partner-contact/issues/new?body=module:%20
partner_contact_vat%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Jairo Llopis <j.llopis@grupoesoc.es>

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
