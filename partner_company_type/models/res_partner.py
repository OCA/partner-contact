# Copyright 2017-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_company_type_id = fields.Many2one(
        comodel_name="res.partner.company.type", string="Legal Form"
    )
