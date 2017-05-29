# -*- coding: utf-8 -*-
# Copyright 2014 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2015 Antonio Espinosa <antonioea@antiun.com>
# Copyright 2015 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Partner job position",
    "summary": "Categorize job positions for contacts",
    "version": "10.0.1.0.0",
    'category': 'Customer Relationship Management',
    "website": "http://www.antiun.com",
    'author': 'Serv. Tecnolog. Avanzados - Pedro M. Baeza, '
              'Antiun Ingeniería S.L., '
              'Tecnativa,'
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/res_partner_job_position_view.xml',
        'views/res_partner_view.xml',
    ],
}
