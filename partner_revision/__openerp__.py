# -*- coding: utf-8 -*-
#
#
#    Authors: Guewen Baconnier
#    Copyright 2015 Camptocamp SA
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
#

{'name': 'Partner Revisions',
 'version': '1.0',
 'author': 'Camptocamp',
 'license': 'AGPL-3',
 'category': 'Sales Management',
 'depends': ['base',
             ],
 'website': 'http://www.camptocamp.com',
 'data': ['security/security.xml',
          'security/ir.model.access.csv',
          'views/menu.xml',
          'views/res_partner_revision_views.xml',
          'views/revision_field_rule_views.xml',
          'views/res_partner_views.xml',
          ],
 'test': [],
 'installable': True,
 'auto_install': False,
 }
