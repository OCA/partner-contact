# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from . import models
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    partners = env["purchase.order"].search([]).mapped("partner_id")
    partners |= partners.mapped("commercial_partner_id")
    partners._increase_rank("supplier_rank")
