.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================================
Exclude some records from the deduplication
===========================================

This module extends the possibilities of the contact deduplication allowing
to filter the applicable set according to several criteria.

For now, only the filter for restricting the deduplication to only companies or
only contacts is implemented.

Usage
=====

To use this module, you need to:

#. Go to *CRM/Sales > Tools > Deduplicate Contacts*.
#. Mark "'Is a company?' field selected", "Parent company not set" or
   "Parent company set (Contacts)" in the section 'Exclude contacts having'.
#. This criteria will be used for excluding in the deduplication the selected
   kind of records.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/111/10.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/crm/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.
* `Funnel <https://openclipart.org/detail/245510/funnel>`_.
* `Arrow <https://openclipart.org/detail/131875/convergent>`_.

Contributors
------------

* Pedro M. Baeza <pedro.baeza@tecnativa.com>
* Vicent Cubells <vicent.cubells@tecnativa.com>
* Luis M. Ontalba <luis.martinez@tecnativa.com>

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
