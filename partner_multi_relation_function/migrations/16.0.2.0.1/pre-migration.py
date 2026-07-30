# Copyright 2026 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

from odoo.tools.sql import column_exists

column_renames = {
    "res_partner_relation": [("function", "contact_function")],
}


@openupgrade.migrate()
def migrate(env, version):
    """Rename the column to prevent a clash with partner_multi_relation_contact."""
    if column_exists(env.cr, "res_partner_relation", "function"):
        openupgrade.rename_columns(env.cr, column_renames)
