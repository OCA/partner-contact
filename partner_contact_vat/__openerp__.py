# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de servicios, S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "VAT in contact partners",
    "summary": "Allow to set up VAT for contacts",
    "version": "8.0.1.0.0",
    "category": "Accounting & Finance",
    "website": "https://grupoesoc.es",
    "author": "Grupo ESOC Ingeniería de servicios, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base_vat",
        "partner_contact_personal_information_page",
    ],
    "images": [
        "images/constraint.png",
        "images/field.png",
    ],
    "data": [
        "view/res_partner.xml",
    ],
}
