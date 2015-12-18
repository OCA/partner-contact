# -*- coding: utf-8 -*-
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#    Copyright (c) 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
#                       Antonio Espinosa <antonioea@antiun.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner job position",
    "summary": "Categorize job positions for contacts",
    "version": "8.0.1.0.0",
    'category': 'Customer Relationship Management',
    "website": "http://www.antiun.com",
    'author': 'Serv. Tecnolog. Avanzados - Pedro M. Baeza, '
              'Antiun Ingeniería S.L., '
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/res_partner_job_position_view.xml',
        'views/res_partner_view.xml',
    ],
}
