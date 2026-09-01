from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # Use `config_parameter` instead of `default_` so we can
    # apply it as the default for existing users
    map_website_id = fields.Many2one(
        comodel_name="map.website",
        string="Map Website",
        config_parameter="partner_external_map.default_map_website_id",
        domain=["|", ("address_url", "!=", False), ("lat_lon_url", "!=", False)],
    )

    route_map_website_id = fields.Many2one(
        comodel_name="map.website",
        string="Route Map Website",
        config_parameter="partner_external_map.default_route_map_website_id",
        domain=[
            "|",
            ("route_address_url", "!=", False),
            ("route_lat_lon_url", "!=", False),
        ],
    )
