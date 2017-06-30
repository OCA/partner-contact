.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================
Default sales discount per partner
==================================

This module allows to define at partner level a default discount to be applied
on sales orders as the default one. As the field is a company dependent one,
you can configure a different value for the partner for each of your companies.

Configuration
=============

Enabling the use of discounts in Odoo:

#. Go to *Sales > Configuration > Settings*
#. On the group "Quotations & Sales", select the option "Allow discounts on
   sales order lines" for the "Discount" section.

Setting a default sales discount:

#. Then, go to *Sales > Customers*.
#. Create or modify a customer.
#. Go to "Sales & Purchases" page.
#. In the "Sale" section, there's a field called "Default sales discount (%)"
   where you can fill the default discount percentage.
#. This value can only be filled at company partners, not for contacts.

Usage
=====

To use this module, you need to:

#. Go to *Sales > Quotations*.
#. Create a new quotation.
#. Select a partner with a default discount applied.
#. Create an order line, and you will see this discount as default in the line.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/134/9.0

Known issues / Roadmap
======================

* This module doesn't work with *product_visible_discount*, as it overwrites
  the discount field with its own value.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/partner-contact/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Pedro M. Baeza <pedro.baeza@tecnativa.com>

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
