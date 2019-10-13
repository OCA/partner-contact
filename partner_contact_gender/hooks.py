# Copyright 2016-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    gender_mappings = {
        "female": env.ref("base.res_partner_title_madam")
        + env.ref("base.res_partner_title_miss"),
        "male": env.ref("base.res_partner_title_mister"),
    }
    for gender, titles in list(gender_mappings.items()):
        env["res.partner"].with_context(active_test=False).search(
            [("title", "in", titles.ids)]
        ).write({"gender": gender})
