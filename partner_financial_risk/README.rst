.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

======================
Partner Financial Risk
======================

Adds a new page in partner to manage its *Financial Risk*.

If any limit is exceeded, you won't be able to confirm any of its invoices
unless you are authorized (Account Adviser group).

Configuration
=============

To configure this module, you need to:

#. Go to *Settings > Configuration > Invoicing*
#. In the *Financial Risk* section, fill *Unpaid Margin* for setting the number
   of days to last after the due date to consider an invoice as unpaid.

Usage
=====

To use this module, you need to:

#. Go to *Invoicing/Accounting > Sales > Customers*.
#. Select an existing customer or create a new one.
#. Open the *Financial Risk* tab.
#. Set limits and choose options to compute in credit limit.
#. Go to *Invoicing/Accounting > Sales > Customer invoices* and create new
   customer invoices.
#. Test the restriction trying to create an invoice for the partner for an
   amount higher of the limit you have set.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/8.0


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

* Carlos Dauden <carlos.dauden@tecnativa.com>
* Pedro M. Baeza <pedro.baeza@tecnativa.com>
* OpenSynergy Indonesia <https://opensynergy-indonesia.com>


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
