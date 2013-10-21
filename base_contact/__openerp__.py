# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2013-TODAY OpenERP S.A. (<http://openerp.com>).
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
    'name': 'Contacts Management',
    'version': '1.0',
    'category': 'Customer Relationship Management',
    'complexity': "expert",
    'description': """
This module allows you to manage your contacts
==============================================

It lets you define groups of contacts sharing some common information, like:
    * Birthdate
    * Nationality
    * Native Language

    """,
    'author': 'OpenERP SA',
    'website': 'http://www.openerp.com',
    'depends': ['base', 'process', 'contacts'],
    'init_xml': [],
    'update_xml': [
        'base_contact_view.xml',
    ],
    'demo_xml': [
        'base_contact_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    #'certificate': '0031287885469',
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
