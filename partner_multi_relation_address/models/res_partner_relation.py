# Copyright 2025 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartnerRelation(models.Model):

    _inherit = "res.partner.relation"

    email = fields.Char()
    phone = fields.Char()
    mobile = fields.Char()
    street = fields.Char()
    zipcode = fields.Char()
    city = fields.Char()
    country_id = fields.Many2one(comodel_name="res.country")
