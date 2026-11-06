# Copyright 2026 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class Base(models.AbstractModel):
    _inherit = "base"

    def _additional_allowed_keys_properties_definition(self):
        return super()._additional_allowed_keys_properties_definition() + (
            "partner_scope",
        )

    def _validate_properties_definition(self, properties_definition, field):
        res = super()._validate_properties_definition(properties_definition, field)
        for definition in properties_definition:
            if definition.get("partner_scope", "all") not in (
                "all",
                "companies",
                "individuals",
            ):
                raise ValueError("Invalid partner property scope")
        return res
