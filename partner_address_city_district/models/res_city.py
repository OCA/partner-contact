# Copyright 2022 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCity(models.Model):
    _inherit = "res.city"

    city_district_ids = fields.One2many('res.city.district', 'city_id')
