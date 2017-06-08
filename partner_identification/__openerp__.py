# -*- coding: utf-8 -*-
#
# © 2004-2010 Tiny SPRL http://tiny.be
# © 2010-2012 ChriCar Beteiligungs- und Beratungs- GmbH
#             http://www.camptocamp.at
# © 2015 Antiun Ingenieria, SL (Madrid, Spain)
#        http://www.antiun.com
#        Antonio Espinosa <antonioea@antiun.com>
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Partner Identification Numbers',
    'category': 'Customer Relationship Management',
    'version': '10.0.1.1.1',
    'depends': [
        'sales_team',
    ],
    'data': [
        'views/res_partner_id_category_view.xml',
        'views/res_partner_id_number_view.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv',
    ],
    'author': 'ChriCar Beteiligungs- und Beratungs- GmbH, '
              'Tecnativa,'
              'Camptocamp,'
              'ACSONE SA/NV,'
              'LasLabs,'
              'Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'installable': True,
}
