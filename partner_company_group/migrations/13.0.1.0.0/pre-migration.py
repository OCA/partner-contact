# Copyright 2021 Tecnativa - Sergio Teruel
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from openupgradelib import openupgrade

field_renames = [
    ("res.partner", "res_partner", "group_id", "company_group_id",),
]


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(env.cr, "res_partner", "group_id"):
        if not openupgrade.column_exists(env.cr, "res_partner", "company_group_id"):
            openupgrade.rename_fields(env, field_renames)
        else:
            openupgrade.logged_query(
                env.cr,
                """
                UPDATE res_partner
                SET company_group_id = group_id
                WHERE company_group_id IS NULL AND group_id IS NOT NULL""",
            )
