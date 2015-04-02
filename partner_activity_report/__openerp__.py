# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Nicolas Bessi. Copyright Camptocamp SA
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
    'description': """
This module give a report with recent activity on the partner
====================================================================

* Display adresses and contact of the partner
* Display crm open for this partner
* Display invoices related to this partner
* Display sale order related to this customer
* Display delivery lines related to this customer


""",
    'version': '1.2',
    'author': "Camptocamp",
    'maintainer': 'Camptocamp',
    'category': 'Extra Tools',
    'website': 'http://www.camptocamp.com',
    'depends': ['base','account','sale','stock'],
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
