# -*- coding: utf-8 -*-
# Copyright 2014-2016 Akretion (Alexis de Lattre
#                     <alexis.delattre@akretion.com>)
# Copyright 2014 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
#                <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Base Location Geonames Import',
    'version': '11.0.1.0.1',
    'category': 'Partner Management',
    'license': 'AGPL-3',
    'summary': 'Import better zip entries from Geonames',
    'author': 'Akretion,'
              'Agile Business Group,'
              'Antiun Ingeniería S.L.,'
              'Tecnativa,'
              'Odoo Community Association (OCA)',
    'website': 'http://www.akretion.com',
    'depends': ['base_location'],
    'external_dependencies': {'python': ['requests']},
    'data': [
        'wizard/geonames_import_view.xml',
        ],
    'installable': True,
}
