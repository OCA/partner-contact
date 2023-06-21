# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    company_id = fields.Many2one(default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        # The context value is set in the create method of res.company
        if self.env.context.get("creating_from_company"):
            vals["company_id"] = False
        return super(ResPartner, self).create(vals)
