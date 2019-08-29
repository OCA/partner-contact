# Copyright 2015-2017 ACSONE SA/NV (<https://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Partner Academic Title",
    'summary': """
        Add possibility to define some academic title""",
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': "https://github.com/OCA/partner-contact",
    'category': 'Other',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/partner_academic_title_data.xml',
        'views/partner_academic_title_view.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
