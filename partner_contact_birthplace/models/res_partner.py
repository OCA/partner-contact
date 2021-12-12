# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    birth_city = fields.Char()
    birth_state_id = fields.Many2one(
        comodel_name="res.country.state", string="Birth state", ondelete="restrict"
    )
    birth_country_id = fields.Many2one(
        comodel_name="res.country", string="Birth country", ondelete="restrict"
    )
