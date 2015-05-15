.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Partner second lastname
=======================

This module was written to extend the functionality of ``partner_firstname`` to
support having a second lastname for contact partners.

In some countries, it's important to have a second last name for contacts.

Contact partners will need to fulfill at least one of the name fields
(*First name*, *First last name* or *Second last name*).

Usage
=====

To use this module, you need to:

* Edit any partner's form.
* Make sure the partner is not a company.
* Enter firstname and lastnames.

If you directly enter the full name instead of entering the other fields
separately (maybe from other form), this module will try to guess the best
match for your input and split it between firstname, lastname and second
lastname.

If the name you enter is in the form *Firstname Lastname1 Lastname2*, it will
be split as such. If you use a comma, it will understand it as *Lastname1
Lastname2, Firstname*.

If you can, always enter it manually please. Automatic guessing could fail for
you easily in some corner cases.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/partner-contact/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback `here
<https://github.com/OCA/partner-contact/issues/new?body=module:%20partner_second_lastname%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* `Grupo ESOC <http://grupoesoc.es>`_:
    * `Jairo Llopis <mailto:j.llopis@grupoesoc.es>`_.

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
