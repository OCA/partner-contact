# -*- coding: utf-8 -*-
#    Copyright (c) 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
#                       Antonio Espinosa <antonioea@antiun.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partners Capital',
    'version': '8.0.1.0.0',
    'category': 'Customer Relationship Management',
    'author': 'Antiun Ingeniería S.L.',
    'website': 'http://www.antiun.com',
    'depends': [
        'base',
    ],
    'data': [
        'views/res_partner_turnover_range_view.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv',
    ],
    "installable": True,
}
