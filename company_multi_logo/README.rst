.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License
Company Multiple Logo
=====================

This module allows to display different logos in reports for a single company.
For each partner, a logo can be selected to be displayed in the reports for this partner.


Configuration
=============

To configure this module, you need to:

 * Install the module, and then modify the Qweb template report.external_layout_header to display the logo.
 * This is what the res.partner method get_company_logo is meant for.
 * e.g. <img t-att-src="'data:image/png;base64,%s' % o.partner_id.get_company_logo(company)"/>

 * Go to Settings -> Companies -> Companies
 * Select your company
 * Go to tab 'Report Configuration'
 * Add your logos. You must select one to be the default logo displayed when no logo is choosen for a partner.


Usage
=====

For each partner with a different logo to display than the default one:
 * In the partner form view, go to the tab 'Report Logos' and select the logo that will appear in reports for this partner.
 * If you are using multi-company, one logo can be selected for each company.

Print your reports as usual


Credits
=======

Contributors
------------

* David DUFRESNE <david.dufresne@savoirfairelinux.com>
* Pierre GAULT <pierre.gault@savoirfairelinux.com>


Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.