# Copyright 2023 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def pre_init_hook(cr):
    """Rename existing views in partner_company_group module"""
    openupgrade.rename_xmlids(
        cr,
        [
            (
                "partner_company_group.view_partner_form",
                "base_partner_company_group.view_partner_form",
            ),
            (
                "partner_company_group.view_res_partner_filter",
                "base_partner_company_group.view_res_partner_filter",
            ),
            (
                "partner_company_group.action_open_group_members",
                "base_partner_company_group.action_open_group_members",
            ),
        ],
    )
