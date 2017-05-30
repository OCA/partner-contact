# -*- coding: utf-8 -*-

#    Author: Nicolas Bessi. Copyright Camptocamp SA
#    Copyright (C)
#       2014:       Agile Business Group (<http://www.agilebg.com>)
#       2015:       Grupo ESOC <www.grupoesoc.es>
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

{
    'name': 'Partner first name and last name',
    'summary': "Split first name and last name for non company partners",
    'version': '8.0.2.2.1',
    "author": "Camptocamp, "
              "Grupo ESOC Ingeniería de Servicios, "
              "ACSONE SA/NV, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    'maintainer': 'Camptocamp, Acsone',
    'category': 'Extra Tools',
    'website': 'https://odoo-community.org',
    'depends': ['base_setup'],
    'data': [
        'views/base_config_view.xml',
        'views/res_partner.xml',
        'views/res_user.xml',
        'data/res_partner.yml',
    ],
    'demo': [],
    'test': [],
    'auto_install': False,
    'installable': True,
    'images': []
}
