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

{'name': 'Partner first name, last name',
 'description':  """Split first name last name on res.partner.
The field name become a stored function field concatenating lastname, firstname
""",
 'version': '1.0',
 'author': 'Camptocamp',
 'category': 'MISC',
 'website': 'http://www.camptocamp.com',
 'depends': ['base'],
 'data': ['partner_view.xml'],
 'demo': [],
 'test': [],
 'auto_install': False,
 'installable': True,
 'images': []
}
