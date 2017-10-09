# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Contact Hierarchy Mapping in relations",
    "version": "10.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "CRM",
    "summary": "Syncs the hierarchy partner's contacts with CRM relations",
    "depends": ['partner_multi_relation'],
    "data": [
        'data/data.xml',
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
