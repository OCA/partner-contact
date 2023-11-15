# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

import logging

from odoo.tools import sql

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """Initialise the code field on res.partner.company.type"""
    if not sql.column_exists(cr, "res_partner_company_type", "code"):
        _logger.info("Create column code on res_partner_company_type")
        cr.execute(
            """
            ALTER TABLE res_partner_company_type ADD COLUMN code varchar;
            """
        )
        _logger.info("Init commercial_partner_id on stock_picking")
        cr.execute(
            """
            UPDATE res_partner_company_type
            SET code = '8888' WHERE code IS NULL;
            """
        )
        _logger.info(f"{cr.rowcount} rows updated in stock_picking")
