# -*- encoding: utf-8 -*-
##############################################################################
#
#    Base Location Geonames Import module for OpenERP
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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
    'version': '0.1',
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'summary': 'Import better zip entries from Geonames',
    'description': """
Base Location Geonames Import
=============================

This module adds a wizard to import better zip entries from Geonames (http://download.geonames.org/export/zip/).

When you start the wizard,
it will ask you to select a country. Then, for the selected country,
it will delete all the current better zip entries, download the latest version
of the list of cities from geonames.org and create new better zip entries.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com>
for any help or question about this module.


Contributors
------------

- Alexis de Lattre <alexis.delattre@akretion.com>
- Lorenzo Battistini <lorenzo.battistini@agilebg.com>
""",
    'author': "Akretion,Odoo Community Association (OCA)",
    'website': 'http://www.akretion.com',
    'depends': ['base_location'],
    'external_dependencies': {'python': ['requests', 'unicodecsv']},
    'data': [
        'wizard/geonames_import_view.xml',
    ],
    'installable': True,
    'active': False,
}
