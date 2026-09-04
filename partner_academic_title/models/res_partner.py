# Copyright 2015-2017 ACSONE SA/NV (<https://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    academic_title_ids = fields.Many2many(
        comodel_name="partner.academic.title",
        relation="partner_academic_title_ref",
        column1="partner_id",
        column2="academic_title_id",
        string="Academic Titles",
    )
    academic_title_display = fields.Char(
        string="Academic Titles",
        compute="_compute_academic_title_display",
        store=True,
    )

    def _get_separator(self):
        return ", "

    @api.depends(
        "academic_title_ids",
        "academic_title_ids.name",
        "academic_title_ids.sequence",
    )
    def _compute_academic_title_display(self):
        for partner in self:
            titles = partner.academic_title_ids.sorted("sequence")
            partner.academic_title_display = partner._get_separator().join(
                titles.mapped("name")
            )
