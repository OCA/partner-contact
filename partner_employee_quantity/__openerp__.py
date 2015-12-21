# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería S.L. - Antonio Espinosa
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Employee quantity in partners',
    'summary': 'Know how many employees a partner has',
    'version': '8.0.1.0.0',
    'category': 'Customer Relationship Management',
    "author": "Antiun Ingeniería S.L., Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    'website': 'http://www.antiun.com',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_employee_quantity_range_view.xml',
        'views/res_partner_view.xml',
    ],
    "installable": True,
}
