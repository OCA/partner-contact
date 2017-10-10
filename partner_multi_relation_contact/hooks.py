# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    partner_model = env['res.partner']
    # Contact relations have to be created for contacts:
    partners = partner_model.with_context(active_test=False).search([
        ('parent_id', '=', True),
        ('is_company', '=',  False),
        ('type', '=',  'contact'),
    ])
    partners.update_relations()
