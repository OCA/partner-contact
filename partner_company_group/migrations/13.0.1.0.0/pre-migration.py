# Copyright 2021 Tecnativa - Sergio Teruel
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from openupgradelib import openupgrade

field_renames = [
    ("res.partner", "res_partner", "group_id", "company_group_id",),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, field_renames)
