# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import SUPERUSER_ID
from odoo.api import Environment
from odoo.tools import config


def post_init_hook(cr, pool):
    """
    We need to activate the rule only if we are not in a test environment.
    """
    if not config["test_enable"]:
        env = Environment(cr, SUPERUSER_ID, {})
        tier_partner = env.ref(
            "partner_tier_validation.partner_tier_definition_company_only"
        )
        tier_partner.write({"active": True})
