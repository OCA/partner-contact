# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Partner CoC',
    'summary': "Adds a field 'Chamber Of Commerce Registration Number' to "
               "partner",
    'version': '7.0.1.0.0',
    'category': 'Web',
    'description':
    """Adds a field 'Chamber Of Commerce Registration Number' to partner.""",
    'author': 'Onestein,Odoo Community Association (OCA)',
    'website': 'https://github.com/oca/partner-contact',
    'license': 'AGPL-3',
    'depends': [
        'partner_identification',
    ],
    'data': [
        'data/res_partner_id_category_data.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'application': False,
}
