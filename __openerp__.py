# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL
#                            http://tiny.be
#    Copyright (C) 2010-2012 ChriCar Beteiligungs- und Beratungs- GmbH
#                            http://www.camptocamp.at
#    Copyright (C) 2015 Antiun Ingenieria, SL (Madrid, Spain)
#                       http://www.antiun.com
#                       Antonio Espinosa <antonioea@antiun.com>
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
    # Addon information
    'name': 'Partner Identification Numbers',
    'category': 'Customer Relationship Management',
    'version': '1.0',
    'depends': [
        'crm',
    ],
    'external_dependencies': {},
    # Views templates, pages, menus, options and snippets
    'data': [
        'views/res_partner_id_category_view.xml',
        'views/res_partner_id_number_view.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv',
    ],
    # Qweb templates
    'qweb': [
    ],
    # Your information
    'author': 'ChriCar Beteiligungs- und Beratungs- GmbH, '
              'Antiun Ingeniería, SL',
    'maintainer': 'ChriCar Beteiligungs- und Beratungs- GmbH, '
                  'Antiun Ingeniería S.L.',
    'website': 'http://www.camptocamp.at, '
               'http://www.antiun.com',
    'license': 'AGPL-3',
    # Technical options
    'demo': [],
    'test': [],
    'installable': True,
    # 'auto_install':False,
    # 'active':True,

}
