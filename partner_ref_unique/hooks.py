# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
import logging

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """Create column using SQL to avoid auto-init updating the table row by row
    :param odoo.sql_db.Cursor cr:
        Database cursor.
    """
    _logger.info("Creating res.company.partner_ref_unique column")
    cr.execute("ALTER TABLE res_company ADD partner_ref_unique varchar NULL;")
    cr.execute(
        "COMMENT ON COLUMN public.res_company.partner_ref_unique "
        "IS 'Unique partner reference for';"
    )
    cr.execute(
        "UPDATE res_company SET partner_ref_unique = 'none';"
    )
    _logger.info(
        "Creating res.partner.partner_ref_unique column with value from "
        "res.company"
    )
    cr.execute("ALTER TABLE res_partner ADD partner_ref_unique varchar NULL;")
    cr.execute(
        "COMMENT ON COLUMN res_partner.partner_ref_unique "
        "IS 'Unique partner reference for';"
    )
    cr.execute(
        "UPDATE res_partner rp "
        "SET partner_ref_unique = rc.partner_ref_unique "
        "FROM res_company rc "
        "WHERE rc.id = rp.company_id;"
    )
