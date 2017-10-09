# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    partner_model = env['res.partner']
    # get all fields with a parent
    partners = partner_model.with_context(active_test=False).search(
        [('parent_id', '!=', False)]
    )
    partners.update_relations()
