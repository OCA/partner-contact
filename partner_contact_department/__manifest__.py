# -*- coding: utf-8 -*-
# Copyright 2014-2015 Tecnativa S.L. - Jairo Llopis
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2017 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Contact department',
    "summary": "Assign contacts to departments",
    'version': '10.0.1.0.0',
    'category': 'Customer Relationship Management',
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    "license": "AGPL-3",
    'website': 'http://www.tecnativa.com',
    "application": False,
    'depends': [
        'sales_team',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_department_view.xml',
        'views/res_partner_view.xml',
    ],
    "installable": True,
}
