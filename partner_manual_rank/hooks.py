# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo.tools import column_exists

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    if not column_exists(cr, "res_partner", "is_customer"):
        _logger.info("Fast populate res_partner.is_customer new field ...")
        cr.execute(
            """
            ALTER TABLE res_partner
            ADD COLUMN is_customer bool;
            """
        )
        cr.execute(
            """
            UPDATE res_partner
                SET is_customer = (coalesce(customer_rank, 0) > 0);
            """
        )

    if not column_exists(cr, "res_partner", "is_supplier"):
        _logger.info("Fast populate res_partner.is_supplier new field ...")
        cr.execute(
            """
            ALTER TABLE res_partner
            ADD COLUMN is_supplier bool;
            """
        )
        cr.execute(
            """
            UPDATE res_partner
                SET is_supplier = (coalesce(supplier_rank, 0) > 0);
            """
        )
