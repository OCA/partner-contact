# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    title_id = fields.Many2one(
        "res.partner.title",
        ondelete="restrict",
        compute="_compute_title_id",
        store=True,
        precompute=True,
        readonly=False,
    )
    # Field 'name_with_title' can be very useful in reports
    name_with_title = fields.Char(compute="_compute_name_with_title")

    @api.depends("is_company")
    def _compute_title_id(self):
        for partner in self:
            if partner.is_company:
                partner.title_id = False

    @api.depends("is_company", "title_id", "name")
    def _compute_name_with_title(self):
        for partner in self:
            name = partner.name
            if not partner.is_company and partner.title_id:
                title = partner.title_id.shortcut or partner.title_id.name
                name = " ".join([title, name])
            partner.name_with_title = name
