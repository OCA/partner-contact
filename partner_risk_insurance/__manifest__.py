# -*- coding: utf-8 -*-
# Copyright 2009 NaN·tic - Albert Cervera
# Copyright 2014 Factor Libre S.L.
# Copyright 2014 AvancOSC - Daniel Campos
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Partner Risk Insurance',
    'version': '10.0.1.0.0',
    'category': 'Sales Management',
    'summary': 'Lets set risk insurance info in the partners',
    'author': 'AvanzOSC,'
              'Factor Libre S.L,'
              'NaN·tic,'
              'Tecnativa,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/partner-contact',
    'license': 'AGPL-3',
    'depends': [
        'partner_financial_risk',
    ],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
