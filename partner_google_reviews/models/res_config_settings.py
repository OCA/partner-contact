# Copyright 2023 NathanQj
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    google_places_api_key = fields.Char(
        string="Google Places API Key",
        config_parameter="partner_google_reviews.google_places_api_key",
        help="Enter your Google Places API key here.",
    )
