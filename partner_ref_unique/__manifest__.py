# Copyright 2016 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner unique reference",
    "summary": "Add an unique constraint to partner ref field",
    "version": "12.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact/",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "views/res_company_view.xml",
    ],
}
