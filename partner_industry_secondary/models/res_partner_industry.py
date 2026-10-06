# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2016 Tecnativa S.L. - Pedro M. Baeza
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# Copyright 2019 Tecnativa - Cristina Martin R.
# Copyright 2025 Moduon - Eduardo de Miguel
# Copyright 2025, 2026 XCG SAS
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models
from odoo.tools import populate


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

    def name_get(self):
        def get_names(cat):
            """Return the list [cat.name, cat.parent_id.name, ...]"""
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.parent_id
            return res

        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_industry_secondary.display_last_child_first")
        ):
            # Display last child first
            result = []
            for cat in self:
                cat_name, *parent_cats = get_names(cat)
                if parent_cats:
                    cat_name = f"{cat_name} ({' < '.join(parent_cats)})"
                result.append((cat.id, cat_name))
            return result
        # Default display (Grandparent / Parent / Child)
        return [(cat.id, " / ".join(get_names(cat)[::-1])) for cat in self]

    @api.constrains("name", "parent_id")
    def _check_uniq_name(self):
        for industry in self:
            if (
                self.search_count(
                    [
                        ("name", "=", industry.name),
                        ("parent_id", "=", industry.parent_id.id),
                    ]
                )
                > 1
            ):
                raise exceptions.ValidationError(
                    _("Error! Industry with same name and parent already exists.")
                )

    def copy(self, default=None):
        default = default or {}
        if "name" not in default or default["name"] == self.name:
            default["name"] = self.name + " 2"
        return super(ResPartnerIndustry, self).copy(default=default)

    def _populate_factories(self):
        result = super()._populate_factories()
        modified_result = []
        # search for name to replace it to avoid empty names
        for field_name, populate_function in result:
            if field_name == "name":
                modified_result.append(
                    (
                        field_name,
                        populate.cartesian(["Industry name {counter}"], [1.0]),
                    )
                )
            else:
                modified_result.append((field_name, populate_function))
        return modified_result
