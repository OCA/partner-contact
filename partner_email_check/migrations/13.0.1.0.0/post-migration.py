# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    param_duplicate = env["ir.config_parameter"].search(
        [("key", "=", "partner_email_check_filter_duplicates")]
    )
    if param_duplicate:
        env["res.company"].search([]).write(
            {"partner_email_check_filter_duplicates": param_duplicate.value}
        )
        param_duplicate.unlink()
    param_deliverability = env["ir.config_parameter"].search(
        [("key", "=", "partner_email_check_check_deliverability")]
    )
    if param_deliverability:
        env["res.company"].search([]).write(
            {"partner_email_check_check_deliverability": param_deliverability.value}
        )
        param_deliverability.unlink()
