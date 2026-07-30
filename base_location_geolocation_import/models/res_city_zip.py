# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCityZip(models.Model):
    """City/locations completion object"""

    _inherit = "res.city.zip"

    latitude = fields.Float(string="Geo Latitude", digits=(10, 7))
    longitude = fields.Float(string="Geo Longitude", digits=(10, 7))
