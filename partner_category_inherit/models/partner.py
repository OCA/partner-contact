# Copyright 2023 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    category_id = fields.Many2many(
        compute="_compute_category_id", store=True, readonly=False
    )

    @api.depends("parent_id", "parent_id.category_id")
    def _compute_category_id(self):
        for record in self:
            for categ in record.parent_id.category_id.filtered("inherited"):
                record.category_id |= categ
            if record.parent_id:
                for categ in record.category_id.filtered("inherited"):
                    if categ not in record.parent_id.category_id:
                        record.category_id -= categ

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        # Apply parent's inherited tags
        partners._compute_category_id()
        return partners

    @api.constrains("category_id")
    def _check_category_inherited_only_on_top_level(self):
        for record in self:
            if record.parent_id:
                for categ in record.category_id.filtered("inherited"):
                    if categ not in record.parent_id.category_id:
                        raise UserError(
                            _(
                                "Inheritable tags should only be put on the top-level partner"
                            )
                        )
