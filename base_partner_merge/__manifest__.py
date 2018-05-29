# Copyright 2016 Camptocamp SA
# Copyright 2017 Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Deduplicate Contacts (No CRM)",
    'version': '11.0.1.0.1',
    'summary': "Partner merge wizard without dependency on CRM",
    'category': 'Generic Modules/Base',
    'author': "Camptocamp,Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/partner-contact',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'views/base_partner_merge.xml',
    ],
    'installable': True,
}
