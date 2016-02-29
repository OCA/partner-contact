# -*- coding: utf-8 -*-
# © 2015 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Customer profit segmentation",
    'images': ['static/description/main_screenshot.png'],
    'summary': """Customer segmentation based on profit""",
    'author': "ONESTEiN BV,Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'website': "http://www.onestein.eu",
    'category': 'Sales',
    'version': '8.0.1.0.0',
    'depends': [
        'account',
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/res_partner_profitseg_segment.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
