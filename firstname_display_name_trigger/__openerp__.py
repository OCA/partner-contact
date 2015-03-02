# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Yannick Vaucher
#    Copyright 2013 Camptocamp SA
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
    'name': ('Link module if partner_lastname and account_report_company are '
             'installed'),
    'version': '1.0',
    'author': "Camptocamp,Odoo Community Association (OCA)",
    'maintainer': 'Camptocamp',
    'category': 'Hidden',
    'license': 'AGPL-3',
    'depends': [
        'account_report_company',
        'partner_firstname',
    ],
    'description': """
Adapt the computation of display name so that it gets visible in tree and
kanban views.
""",
    'website': 'http://www.camptocamp.com',
    'data': [],
    'installable': True,
    'auto_install': True,
    'application': False,
}
