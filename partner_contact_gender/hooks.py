# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, pool):
    env = api.Environment(cr, SUPERUSER_ID, {})
    gender_mappings = {
        'female': env.ref('base.res_partner_title_madam') +
        env.ref('base.res_partner_title_miss'),
        'male': env.ref('base.res_partner_title_mister')
    }
    for gender, titles in gender_mappings.iteritems():
        env['res.partner'].with_context(active_test=False).search([
            ('title', 'in', titles.ids),
        ]).write({
            'gender': gender,
        })
