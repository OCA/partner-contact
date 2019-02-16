# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Partner Company Type',
    'summary': 'Adds a company type to partner that are companies',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/partner-contact',
    'depends': [
        'contacts',
    ],
    'data': [
        'security/res_partner_company_type.xml',
        'views/res_partner_company_type.xml',
        'views/res_partner.xml',
    ],
    'demo': [
        'demo/res_partner_company_type.xml',
    ],
}
