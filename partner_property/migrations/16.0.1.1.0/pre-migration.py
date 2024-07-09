# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """Convert the old key to the new one and duplicate for person."""
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_config_parameter
        SET key = 'partner_property.properties_definition_company'
        WHERE key = 'partner_property.properties_definition'
        """,
    )
    icp = env["ir.config_parameter"].search(
        [("key", "=", "partner_property.properties_definition_company")]
    )
    icp.copy({"key": "partner_property.properties_definition_person"})
