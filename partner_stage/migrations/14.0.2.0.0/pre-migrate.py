# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tools.sql import column_exists, rename_column


def migrate(cr, version):
    if column_exists(cr, "res_partner", "state"):
        if column_exists(cr, "res_partner", "old_state"):
            cr.execute("ALTER TABLE res_partner DROP COLUMN old_state")
        rename_column(cr, "res_partner", "state", "old_state")
