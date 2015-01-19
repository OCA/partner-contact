# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Nicolas Bessi. Copyright Camptocamp SA
#    Contributor: Pedro Manuel Baeza <pedro.baeza@serviciosbaeza.com>
#                 Ignacio Ibeas <ignacio@acysos.com>
#                 Alejandro Santana <alejandrosantana@anubia.es>
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
    'name': 'Location management (aka Better ZIP)',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Camptocamp',
    'license': "AGPL-3",
    'contributors': [
        'Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>',
        'Ignacio Ibeas (Acysos S.L.)',
        'Alejandro Santana <alejandrosantana@anubia.es>',
    ],
    'summary': '''Enhanced zip/npa management system''',
    'description': '''
    This module introduces a better zip/npa management system.
    It enables zip, city, state and country auto-completion on partners and 
    companies.
    Also allows different search filters.''',
    'website': 'http://www.camptocamp.com',
    'data': ['views/better_zip.xml',
             'views/state.xml',
             'views/res_country.xml',
             'views/company.xml',
             'views/partner.xml',
             'security/ir.model.access.csv'],
    'installable': True,
    'active': False,
}
