# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2016 Tecnativa S.L. - Pedro M. Baeza
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# Copyright 2019 Tecnativa - Cristina Martin R.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models


class ResPartnerIndustry(models.Model):
    _inherit = "res.partner.industry"
    _order = "parent_path"
    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char(required=True)
    parent_id = fields.Many2one(
        comodel_name="res.partner.industry", ondelete="restrict"
    )
    child_ids = fields.One2many(
        comodel_name="res.partner.industry", inverse_name="parent_id", string="Children"
    )
    parent_path = fields.Char(index=True, unaccent=False)

    @api.depends("name", "parent_id", "parent_id.display_name")
    def _compute_display_name(self):
        for rec in self:
            if rec.parent_id:
                rec.display_name = f"{rec.parent_id.display_name} / {rec.name}"
            else:
                rec.display_name = rec.name

    @api.constrains("name", "parent_id")
    def _check_uniq_name(self):
        if (
            self.search_count(
                [("name", "=", self.name), ("parent_id", "=", self.parent_id.id)]
            )
            > 1
        ):
            raise exceptions.ValidationError(
                _("Error! Industry with same name and parent already exists.")
            )

    def copy(self, default=None):
        default = default or {}
        if "name" not in default or default["name"] == self.name:
            default["name"] = f"{self.name} 2"
        return super().copy(default=default)
