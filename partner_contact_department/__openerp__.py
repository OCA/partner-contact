# -*- coding: utf-8 -*-
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#    Copyright (c) 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
#                       Antonio Espinosa <antonioea@antiun.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Contact department',
    "summary": "Assign contacts to departments",
    'version': '8.0.1.0.0',
    'category': 'Customer Relationship Management',
    'author': 'Serv. Tecnol. Avanzados - Pedro M. Baeza, '
              'Antiun Ingeniería S.L., '
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    'website': 'http://www.antiun.com',
    "application": False,
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_department_view.xml',
        'views/res_partner_view.xml',
    ],
    "installable": True,
}
