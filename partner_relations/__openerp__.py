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
    "version": "1.1",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "complexity": "normal",
    "description": """
Introduction
------------

This addon aims to provide generic means to model relations between partners.

Examples would be 'is sibling of' or 'is friend of', but also 'has contract X
with' or 'is assistant of'. This way, you can enode your knowledge about your
partners directly in your partner list.

Usage
-----

Before being able to use relations, you'll have define some first. Do that in
Sales / Configuration / Address Book / Partner relations. Here, you need to
name both sides of the relation: To have an assistant-relation, you would name
one side 'is assistant of' and the other side 'has assistant'. This relation
only makes sense between people, so you would choose 'Person' for both partner
types. For the relation 'is a competitor of', both sides would be companies,
while the relation 'has worked for' should have persons on the left side and
companies on the right side. If you leave this field empty, the relation is
applicable to all types of partners.

If you use categories to further specify the type of partners, you could for
example enforce that the 'is member of' relation can only have companies with
label 'Organization' on the left side.

Now open a partner and choose relations as appropriate in the 'Relations' tab.

Searching partners with relations
---------------------------------

Searching for relations is integrated transparently into the partner search
form. To find all assistants in your database, fill in 'is assistant of' and
autocomplete will propose to search for partners having this relation. Now if
you want to find Anna's assistant, you fill in 'Anna' and one of the proposals
is to search for partners having a relation with Anna. This results in Anna's
assistant(s), as you searched for assistants before.

By default, only active, not expired relations are shown. If you need to find
partners that had some relation at a certain date, fill in that date in the
search box and one of the proposals is to search for relations valid at that
date.""",
    "category": "Customer Relationship Management",
    "depends": [
        'base',
        'web_m2x_options',
        'web_tree_many2one_clickable',
    ],
    "demo": [
        "data/demo.xml",
    ],
    "data": [
        "view/res_partner_relation_all.xml",
        'view/res_partner.xml',
        'view/res_partner_relation.xml',
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
