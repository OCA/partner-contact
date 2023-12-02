#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging


def pre_init_hook(cr):
    logger = logging.getLogger(__name__)
    logger.info("Create a new field display_name_en")
    cr.execute(
        """
        ALTER TABLE res_partner
        ADD COLUMN IF NOT EXISTS display_name_en character varying;
        """
    )
    logger.info("Copy display_name to display_name_en field")
    cr.execute("UPDATE res_partner SET display_name_en=display_name;")
