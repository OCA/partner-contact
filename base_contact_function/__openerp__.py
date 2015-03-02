# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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
    'name': 'Contact by Function',
    'version': '1.0',
    'author': "Savoir-faire Linux,Odoo Community Association (OCA)",
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'category': 'Customer Relationship Management',
    'description': """
Contacts by Functions
=====================

This module allows you to manage contacts by functions.

A person can occupy many job positions in many organizations and you may need
to retrieve all your contacts for a given job position.

This module replaces the single "job position" field on a contact and gives
the possibility to declare many functions (i.e job positions) for a contact.
You can also manage the functions on the organization
(res.partner is_company=True) itself.

To retrieve contacts by functions, categories (tags) are used in order to group
similar functions in a single category. Within a category, you can declare
the sequence of functions so you could use this sequence to sort the contacts
of this category by their function.

When you have functions for your contacts and functions for the categories you
can tag the contacts (manually or automatically with the segmentation tool) and
search with the tag name.

E.g.:
You may need to have a category such as 'Head of State' to quickly identify
contacts that occupies the functions 'President', 'Prime minister' or 'King'.
For protocol reasons, you may want to have 'Kings' sorted first.

Contributors
------------
* El Hadji Dem (elhadji.dem@savoirfairelinux.com)
* Sandy Carter (sandy.carter@savoirfairelinux.com)
""",
    'depends': [
        'base_contact',
    ],
    'data': [
        'res_partner_function_view.xml',
        'res_partner_category_view.xml',
        'res_partner_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
