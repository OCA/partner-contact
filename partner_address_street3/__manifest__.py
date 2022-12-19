# Copyright 2014-2020 Camptocamp SA
# @author: Nicolas Bessi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Street3 in addresses",
    "summary": "Add a third address line on partners",
    "license": "AGPL-3",
    "version": "16.0.1.0.0",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "maintainer": "Camptocamp",
    "category": "Sales",
    "depends": ["base_view_inheritance_extension"],
    "website": "https://github.com/OCA/partner-contact",
    "data": ["views/res_partner.xml"],
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "installable": True,
}
