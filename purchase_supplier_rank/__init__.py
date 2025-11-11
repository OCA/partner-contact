# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from . import models
from odoo import api, SUPERUSER_ID
import os


def post_init_hook(env):
    if (
        os.getenv("ODOO_TEST_MODE")
        or getattr(env, "registry", None)
        and getattr(env.registry, "in_test_mode", False)
    ):
        return

    envs = api.Environment(env.cr, SUPERUSER_ID, {})
    partners = envs["purchase.order"].search([]).mapped("partner_id")
    partners |= partners.mapped("commercial_partner_id")
    partners._increase_rank("supplier_rank")
