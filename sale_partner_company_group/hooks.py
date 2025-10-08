# Copyright 2022 Tecnativa - V??ctor Mart??nez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo.tools.sql import column_exists


def pre_init_hook(env):
    """Prepopulate stored related fields for faster installation"""
    if not column_exists(env.cr, "sale_order", "company_group_id"):
        logger = logging.getLogger(__name__)
        logger.info("Prepopulating stored related fields")
        env.cr.execute(
            """
            ALTER TABLE sale_order
            ADD COLUMN company_group_id integer;
            """
        )
