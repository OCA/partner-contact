# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartnerIndustry(models.Model):

    _inherit = 'res.partner.industry'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name', store=True
    )
    parent_path = fields.Char(index=True)
    parent_id = fields.Many2one(comodel_name="res.partner.industry")
    child_ids = fields.One2many(
        comodel_name="res.partner.industry",
        inverse_name="parent_id",
        string="Children Industry",
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for industry in self:
            if industry.parent_id:
                industry.complete_name = '%s / %s' % (
                    industry.parent_id.complete_name,
                    industry.name,
                )
            else:
                industry.complete_name = industry.name
