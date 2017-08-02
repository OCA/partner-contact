# -*- coding: utf-8 -*-
# Copyright 2013-2014 Savoir-faire Linux
#   (<http://www.savoirfairelinux.com>).
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partner Phone Number Extension',
    'version': '10.0.1.0.0',
    'category': 'Customer Relationship Management',
    'summary': 'Partner Phone Number Extension',
    'author': "Savoir-faire Linux, "
              "Eficent, "
              "SerpentCS, "
              "Odoo Community Association (OCA)",
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    "depends": ["base"],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
