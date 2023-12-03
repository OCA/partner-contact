# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from openupgradelib import openupgrade


def pre_init_hook(cr):
    """Prepopulate stored related fields for faster installation"""
    logger = logging.getLogger(__name__)
    logger.info("Prepopulating stored related fields")
    cr.execute(
        """
        ALTER TABLE crm_lead
        ADD COLUMN IF NOT EXISTS company_group_id integer;
        """
    )
    # Rename existing views in partner_company_group module
    openupgrade.rename_xmlids(
        cr,
        [
            (
                "partner_company_group.view_crm_case_opportunities_filter",
                "crm_partner_company_group.view_crm_case_opportunities_filter",
            ),
        ],
    )
