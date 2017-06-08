# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
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
    'name': 'Company Multiple Logo',
    'version': '0.1',
    'author': 'Savoir-faire Linux,Odoo Community Association (OCA)',
    'maintainer': 'Odoo Community Association (OCA)',
    'website': 'http://odoo-community.org',
    'license': 'AGPL-3',
    'category': 'Others',
    'summary': 'Display different logos per company in reports',
    'depends': [
        'base',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
