# Copyright 2017-2018 Onestein (<https://www.onestein.eu>)
# Copyright 2018 Therp BV (<https://www.therp.nl>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Certificate of Conduct',
    'summary': "Adds field 'Certificate of Conduct'",
    'version': '11.0.1.0.0',
    'category': 'CRM',
    'author': 'Therp BV,Onestein,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/partner-contact/',
    'license': 'AGPL-3',
    'depends': [
        'partner_identification',
    ],
    'data': [
        'data/res_partner_id_category_data.xml',
        'views/res_partner_view.xml'
    ],
    'installable': True,
}
