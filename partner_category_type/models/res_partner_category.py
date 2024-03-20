# Copyright 2023 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerCategory(models.Model):
    _inherit = "res.partner.category"

    def _get_category_type_selection(self):
        return [("generic", _("Generic"))]

    def _get_default_category_type(self):
        return "generic"

    category_type = fields.Selection(
        string="Type",
        selection="_get_category_type_selection",
        required=True,
        default=_get_default_category_type,
        compute="_compute_category_type",
        inverse="_inverse_category_type",
        store=True,
    )

    @api.constrains("parent_id", "category_type")
    def _check_parent_type(self):
        for rec in self:
            if rec.parent_id and rec.parent_id.category_type != rec.category_type:
                raise ValidationError(
                    _(
                        "Contact Tag '%(tag_name)s' has different type than "
                        "parent '%(parent_name)s'.",
                        tag_name=rec.name,
                        parent_name=rec.parent_id.name,
                    )
                )

    @api.depends("parent_id")
    def _compute_category_type(self):
        default_category = self._get_default_category_type()
        for rec in self:
            if rec.parent_id:
                rec.category_type = rec.parent_id.category_type
            else:
                rec.category_type = default_category

    def _inverse_category_type(self):
        for rec in self:
            if rec.child_ids:
                rec.child_ids.write({"category_type": rec.category_type})
