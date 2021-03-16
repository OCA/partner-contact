# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from . import models
from odoo.tools.sql import column_exists


def pre_init_hook(cr):
    if not column_exists(cr, "res_partner", "is_customer"):
        cr.execute(
            """
            ALTER TABLE res_partner
            ADD COLUMN is_customer boolean""",
        )
        cr.execute(
            """
            UPDATE res_partner
            SET is_customer = customer_rank::boolean
            """
        )
    if not column_exists(cr, "res_partner", "is_supplier"):
        cr.execute(
            """
            ALTER TABLE res_partner
            ADD COLUMN is_supplier boolean""",
        )
        cr.execute(
            """
            UPDATE res_partner
            SET is_supplier = supplier_rank::boolean
            """
        )
