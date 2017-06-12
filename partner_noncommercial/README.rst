.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Partner Non Commercial
======================

This module changes menu and view descriptions to make partner management
suitable for use in non commercial organisations.

Installation
============

Installing this module needs no special actions.

Configuration
=============

This module requires no special configuration.

Usage
=====

This module changes the Sales main menu to relations. There it gives special
options to work with persons or organisationss.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/partner-contact/8.0

.. repo_id is available in https://github.com/OCA/maintainer-tools/blob/master/tools/repos_with_ids.txt
.. branch is "8.0" for example

Known issues / Roadmap
======================

After installing this module a situation has been encountered where the new
menu's were added to the database, but not shown in the UI. This was due to
partner_left and partner_right not being filled. To solve this, use the
generic solution when the menu-system has been messed up:
  1. stop server
  2. drop parent_left and parent_right columns frm ir_ui_menu table
  3. start server while updating base module


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

* Ronald Portier <ronald@therp.nl>

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
