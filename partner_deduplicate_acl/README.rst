.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Deduplicate Contacts ACL
========================

This module extends the functionality of the CRM contact deduplicator to add
permission groups that allow the matching users to use those tools, not
needing to be the sale settings manager.

Configuration
=============

To configure this module, you need to:

#. Go to *Settings > Users > Users*.
#. Choose a user.
#. Choose the desired permission level(s) in *Appplication > Deduplicate
   Contacts*:

   - *Manually* allows him to do the manual deduplication process.
   - *Automatically* allows him to do the automatic deduplication process.

     .. warning::
         Automatic contact deduplication can easily lead to unwanted results.
         Better backup before doing it.

   - *Without restrictions* executes the chosen deduplication method with admin
     rigts, to be able to update objects where the user would normally not have
     write rights, and to allow him to merge contacts with different email
     addresses.

     .. warning::
        This is an advanced feature, be sure to train the user before enabling
        this permission for him.

Usage
=====

To use this module, you need to:

#. Ask your admin to give you the new rigts.
#. Go to *Sales > Tools > Deduplicate Contacts* as usual.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/111/8.0

Known issues / Roadmap
======================

* Wizard's code is partially written in old API because somehow [possibly]
  the upstream's ``@mute_logger`` decorator prevents API from doing its magic.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/crm/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
crm/issues/new?body=module:%20
crm_deduplicate_acl%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Images
------

* `Arrow <https://openclipart.org/detail/131875/convergent>`_.
* `Lock <http://fontawesome.io/icon/unlock-alt/>`_.

Contributors
------------

* Rafael Blasco <rafabn@antiun.com>
* Jairo Llopis <yajo.sk8@gmail.com>

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
