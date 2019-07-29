# Copyright 2014-2016 Akretion (Alexis de Lattre
#                     <alexis.delattre@akretion.com>)
# Copyright 2014 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
#                <contact@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Base Location Geonames Import',
    'version': '12.0.1.0.1',
    'category': 'Partner Management',
    'license': 'AGPL-3',
    'summary': 'Import zip entries from Geonames',
    'author': 'Akretion,'
              'Agile Business Group,'
              'Tecnativa,'
              'AdaptiveCity,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/partner-contact',
    'depends': [
        'base_location',
    ],
    'data': [
        'data/res_country_data.xml',
        'views/res_country_view.xml',
        'wizard/geonames_import_view.xml',
    ],
    'installable': True,
}
