# Copyright 2021 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Zone',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'KMEE,Odoo Community Association (OCA)',
    'website': 'https://github.com/oca/partner-contact',
    'depends': [
        'contacts',
    ],
    'data': [
        'data/partner_zone_type.xml',

        'security/res_groups.xml',
        'security/ir.model.access.csv',

        'views/partner_zone_menu.xml',
        'views/partner_zone.xml',
        'views/partner_zone_type.xml',
        'views/res_partner.xml',
    ],
    'demo': [
        'demo/res_partner.xml',
        'demo/partner_zone.xml',
    ],
}
