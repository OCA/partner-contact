=======================
USPS Address Validation
=======================


.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1| |badge2|

This module adds a tool to the Contacts page which validates the contact's address. Simply click the 'Validate' button, and the address of the contact will be compared to the USPS address database. The result will be a cleaned address, including the full 9 digit zipcode, in the exact format recognized by USPS

**Table of contents**

.. contents::
   :local:

Configuration
=============

In the *General Settings* menu, enter your USPS API credentials under USPS Address Validation Settings


Usage
=====

On a contact, enter as much of the address as possible to ensure an accurate match. Required are address, and either city/state or zipcode. Click the Validate button to bring up the wizard. User entered text appears on the left as the original address, and the right displays the USPS cleansed address, which may be edited as needed. Either accept or cancel the changes to return to the contact page.


Known issues / Roadmap
======================

* There are no knows issues at this time
* USPS will always return the address in all caps. CamelCase support is not planned for future releases.

Bug Tracker
===========


Credits
=======

Authors
~~~~~~~

* ckolobow

Contributors
~~~~~~~~~~~~

* Craig Kolobow <ckolobow@opensourceintegrators.com>

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-ckolobow| image:: https://github.com/ckolobow.png?size=40px
    :target: https://github.com/ckolobow
    :alt: ckolobow

Current `maintainer <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-ckolobow| 

This module is part of the `OCA/partner-contact <https://github.com/OCA/sale-workflow/tree/15.0/partner_usps_address_validation>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
