# Copyright 2023 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class District(models.Model):
    _name = "res.district"
    _description = "District"
    _order = "name"
    _rec_names_search = ["name", "code"]

    name = fields.Char(required=True)
    code = fields.Char()
    city_id = fields.Many2one(comodel_name="res.city", required=True)
