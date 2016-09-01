.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
Multiple Images in Partners
===========================

This module implements the possibility to have multiple images for a partner.

Installation
============

To install this module, you need to:

* Install ``base_multi_image`` from
  `OCA/server-tools <https://github.com/OCA/server-tools>`_.

Usage
=====

To use this module, you need to:

#. Go to *Sales > Sales > Customers* and choose a partner.
#. Go to the new *Images* tab.
#. Add a new image.
#. Refresh the page.
#. The first image in the collection is the main image for the partner.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/135/9.0

Known issues / Roadmap
======================

* If you try to sort images before saving the partner, you will get an error
  similar to ``DataError: invalid input syntax for integer:
  "one2many_v_id_62"``. This bug has not been fixed yet, but a workaround is
  to save and edit again to sort images.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/partner-contact/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Original implementation
-----------------------
This module is inspired in previous module *product_images* from OpenLabs
and Akretion.


Contributors
------------

* Sharoon Thomas
* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
* Rafael Blasco <rafabn@antiun.com>
* Jairo Llopis <yajo.sk8@gmail.com>
* Sodexis <dev@sodexis.com>
* Sergio Teruel <sergio.teruel@tecnativa.com>

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
