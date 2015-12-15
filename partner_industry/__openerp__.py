# -*- coding: utf-8 -*-
# © 2015 Jacques-Etienne Baudoux <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Partner Industry Sector',
    'version': '8.0.1.0',
    'author': "BCIM,Odoo Community Association (OCA)",
    'category': 'Sales Management',
    'depends': ['base'],
    'website': 'http://www.bcim.be',
    'data': [
        'view/industry.xml',
        'view/partner.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'application': False,
    'images': [],
}
