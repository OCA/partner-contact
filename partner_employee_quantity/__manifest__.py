# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2015 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Employee quantity in partners",
    "summary": "Know how many employees a partner has",
    "version": "16.0.1.0.1",
    "category": "Customer Relationship Management",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_employee_quantity_range_view.xml",
        "views/res_partner_view.xml",
    ],
    "development_status": "Mature",
    "maintainers": ["pedrobaeza", "rafaelbn", "edlopen"],
    "installable": True,
}
