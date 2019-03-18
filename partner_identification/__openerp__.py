# -*- coding: utf-8 -*-
#
# Copyright 2004-2010 Tiny SPRL http://tiny.be
# Copyright 2010-2012 ChriCar Beteiligungs- und Beratungs- GmbH
#             http://www.camptocamp.at
# Copyright 2015 Antiun Ingenieria, SL (Madrid, Spain)
#        http://www.antiun.com
#        Antonio Espinosa <antonioea@antiun.com>
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# Copyright 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Partner Identification Numbers',
    'category': 'Customer Relationship Management',
    'description': """Manage partner identifications.

    This includes searching partners on identification, and also a
    framework for adding identification fields for specific types of
    identification (passpost, drivers license, chamber of commerce id...),
    with common methods to maintain those fields.
    """,
    'version': '7.0.1.1.1',
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
