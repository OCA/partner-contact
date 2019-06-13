# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2015 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partners Capital',
    'version': '12.0.1.0.0',
    'category': 'Customer Relationship Management',
    'license': 'AGPL-3',
    'author': 'Antiun Ingeniería S.L., '
              'Tecnativa, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/partner-contact',
    'depends': [
        'contacts',
    ],
    'data': [
        'views/res_partner_turnover_range_view.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv',
    ],
    "installable": True,
}
