# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from . import models


def post_init_hook(env):
    partners = env["sale.order"].search([]).mapped("partner_id")
    partners |= partners.mapped("commercial_partner_id")
    for partner in partners:
        partner._increase_rank("customer_rank", partner.sale_order_count)
