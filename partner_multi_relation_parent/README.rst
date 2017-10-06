.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=============================================
Parent contact Hierarchy Mapping in relations
=============================================

This module maps automatically the relations between parent partners and their
children as relations. It has an init hook that will create such relations for
existing partners and their children partner. If a child partner changes it's
parent the relation mapping will update automatically. It will automatically
create the relations "has contact" and "is contact of" for partners and their
contacts. This will allow to search using this key, and therefore have an
updated search option for partners and their contacts.



Known issues / Roadmap
======================

* hide/forbade the delition of the "Is contact of" and "Has Contact" installed
  relation types

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/partner_multi_relation/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Giovanni Francesco Capalbo <giovanni@therp.nl>  

Do not contact contributors directly about help with questions or problems concerning this addon, but use the `community mailing list <mailto:community@mail.odoo.com>`_ or the `appropriate specialized mailinglist <https://odoo-community.org/groups>`_ for help, and the bug tracker linked in `Bug Tracker`_ above for technical issues.

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
