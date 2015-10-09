# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Partner relations",
    "version": "8.0.1.1.0",
    "author": "Therp BV,Camptocamp,Odoo Community Association (OCA)",
    "complexity": "normal",
    "category": "Customer Relationship Management",
    "depends": [
        'base',
    ],
    "demo": [
        "data/demo.xml",
    ],
    "test": [
        "test/test_allow.yml",
        # "test/test_disallow.yml",
    ],
    "data": [
        "view/res_partner_relation_all.xml",
        'view/res_partner_relation.xml',
        'view/res_partner.xml',
        'view/res_partner_relation_type.xml',
        'view/menu.xml',
        'security/ir.model.access.csv',
    ],
    "js": [
    ],
    "css": [
    ],
    "qweb": [
    ],
    "auto_install": False,
    "installable": True,
    "external_dependencies": {
        'python': [],
    },
}
