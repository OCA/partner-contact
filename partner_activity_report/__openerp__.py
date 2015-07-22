# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Vincent Renaville, Damien Crier
#    Copyright 2014-2015 Camptocamp SA
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
    'name': 'Partner Activity Details',
    'summary': "This module give a report with recent activity on the partner",
    'version': '1.2',
    'author': "Camptocamp, Odoo Community Association (OCA)",
    'maintainer': 'Odoo Community Association (OCA)',
    'category': 'Extra Tools',
    'website': 'http://www.camptocamp.com',
    'depends': ['base', 'account', 'sale', 'stock', 'crm'],
    'data': [
        'wizard/partner_activity_selection.xml',
        'views/report_partner_activity.xml',
        'report.xml'
    ],
    'demo': [],
    'test': [],
    'auto_install': False,
    'installable': True,
    'images': []
}
