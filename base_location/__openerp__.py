# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Nicolas Bessi. Copyright Camptocamp SA
#    Contributor: Pedro Manuel Baeza <pedro.baeza@serviciosbaeza.com>
#                 Ignacio Ibeas <ignacio@acysos.com>
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
{'name': 'Location management (aka Better ZIP)',
 'version': '1.0',
 'depends': ['base'],
 'author': "Camptocamp,Odoo Community Association (OCA)",
 'description': """
Introduces a better zip/npa management system.
It enables zip/city auto-completion on partners""",
 'website': 'http://www.camptocamp.com',
 'data': ['better_zip_view.xml',
          'state_view.xml',
          'company_view.xml',
          'partner_view.xml',
          'security/ir.model.access.csv'],
 'installable': True,
 'active': False,
 }
