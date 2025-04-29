# Copyright 2013 Nicolas Bessi (Camptocamp SA)
# Copyright 2014 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 Grupo ESOC (<http://www.grupoesoc.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ResUser(models.Model):
    _inherit = "res.users"

    @api.model
    def default_get(self, fields_list):
        """Invert name when getting default values."""
        result = super().default_get(fields_list)

        partner_model = self.env["res.partner"]
        inverted = partner_model._get_inverse_name(
            partner_model._get_whitespace_cleaned_name(result.get("name", "")),
            result.get("is_company", False),
        )

        for field in list(inverted.keys()):
            if field in fields_list:
                result[field] = inverted.get(field)

        return result

    @api.onchange("firstname", "lastname")
    def _compute_name(self):
        """Write the 'name' field according to splitted data."""
        for rec in self:
            rec.name = rec.partner_id._get_computed_name(rec.lastname, rec.firstname)

    def copy(self, default=None):
        default_ = default or {}
        records = self.browse()
        for record in self:
            default = dict(default_)
            if ("name" not in default) and ("partner_id" not in default):
                default["name"] = self.env._("%(name)s (copy)", name=record.name)
            if "login" not in default:
                default["login"] = self.env._("%(login)s (copy)", login=record.login)
            if (
                ("firstname" not in default)
                and ("lastname" not in default)
                and ("name" in default)
            ):
                default.update(
                    self.env["res.partner"]._get_inverse_name(default["name"], False)
                )
            records |= super(ResUser, record).copy(default)
        return records
