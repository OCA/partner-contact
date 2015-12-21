# -*- coding: utf-8 -*-
##############################################################################
#
#    Base Location Geonames Import module for OpenERP
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#    Copyright (C) 2014 Agile Business Group (http://www.agilebg.com)
#    @author Lorenzo Battistini <lorenzo.battistini@agilebg.com>
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
    'name': 'Base Location Geonames Import',
    'version': '8.0.0.3.0',
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'summary': 'Import better zip entries from Geonames',
    'author': 'Akretion,'
              'Agile Business Group,'
              'Antiun Ingeniería S.L.,'
              'Serv. Tecnol. Avanzados - Pedro M. Baeza,'
              'Odoo Community Association (OCA)',
    'website': 'http://www.akretion.com',
    'depends': ['base_location'],
    'external_dependencies': {'python': ['requests', 'unicodecsv']},
    'data': [
        'wizard/geonames_import_view.xml',
        ],
    'test': [
        'test/import.yml'
        ],
    'installable': True,
    'active': False,
}
