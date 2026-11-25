# Copyright 2026 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from uuid import NAMESPACE_URL, uuid5

from openupgradelib import openupgrade

from odoo.tools import SQL


@openupgrade.migrate()
def migrate(env, version):
    parameters = env["ir.config_parameter"].sudo()
    container = env["properties.base.definition"]._get_definition_for_property_field(
        "res.partner", "properties"
    )
    definitions = list(container.properties_definition)
    used_names = {definition["name"] for definition in definitions}
    legacy_columns = []
    parameter_keys = []
    for kind, scope in (("company", "companies"), ("person", "individuals")):
        key = f"partner_property.properties_definition_{kind}"
        parameter_keys.append(key)
        raw = parameters.get_str(key)
        legacy_definitions = json.loads(raw) if raw else []
        column = f"properties_type_{kind}"
        has_column = openupgrade.column_exists(env.cr, "res_partner", column)
        if has_column:
            legacy_columns.append(("res_partner", column))
        for original in legacy_definitions:
            definition = dict(original)
            old_name = definition["name"]
            if "view_in_kanban" in definition:
                definition["view_in_cards"] = definition.pop("view_in_kanban")
            # Keep identifiers separate from native and other legacy properties.
            attempt = 0
            while True:
                name = uuid5(
                    NAMESPACE_URL, f"partner_property:{kind}:{old_name}:{attempt}"
                ).hex[:16]
                if definition["type"] == "html":
                    name += "_html"
                if name not in used_names:
                    break
                attempt += 1
            used_names.add(name)
            definition["name"] = name
            if definition["type"] != "separator":
                definition["partner_scope"] = scope
            definitions.append(definition)
            if has_column:
                env.cr.execute(
                    SQL(
                        "UPDATE res_partner SET properties = "
                        "COALESCE(properties, '{}'::jsonb) "
                        "|| jsonb_build_object(%s::text, %s -> %s) "
                        "WHERE %s ? %s",
                        name,
                        SQL.identifier(column),
                        old_name,
                        SQL.identifier(column),
                        old_name,
                    )
                )
    container.properties_definition = definitions
    env["res.partner"].invalidate_model(["properties"])
    if legacy_columns:
        openupgrade.rename_columns(
            env.cr,
            {
                "res_partner": [
                    (column, f"{column}_old") for _, column in legacy_columns
                ],
            },
        )
    for key in parameter_keys:
        parameter = parameters.search([("key", "=", key)])
        if parameter:
            parameter.key = f"{key}_old"
