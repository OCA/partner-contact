# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Company Group",
    "summary": "Adds the possibility to add a company group to a company",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "author": "Camptocamp SA, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "maintainers": ["luisg123v"],
    "depends": [
        "account_partner_company_group",
        "crm_partner_company_group",
        "sale_partner_company_group",
    ],
    "website": "https://github.com/OCA/partner-contact",
    "data": [
        "views/opportunity_view.xml",
        "views/contact_view.xml",
        "views/sale_order_view.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
}
