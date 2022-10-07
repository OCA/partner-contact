# Copyright 2022 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    usps_api_url = fields.Char(
        string="API URL",
        default="https://secure.shippingapis.com/ShippingAPI.dll",
        config_parameter="usps_api_url",
    )
    usps_username = fields.Char(string="Username", config_parameter="usps_username")
    usps_password = fields.Char(string="Password", config_parameter="usps_password")

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            usps_api_url=self.env["ir.config_parameter"]
            .sudo()
            .get_param("usps_api_url"),
            usps_username=self.env["ir.config_parameter"]
            .sudo()
            .get_param("usps_username"),
            usps_password=self.env["ir.config_parameter"]
            .sudo()
            .get_param("usps_password"),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env["ir.config_parameter"].sudo()
        usps_api_url = self.usps_api_url
        usps_username = self.usps_username
        usps_password = self.usps_password
        param.set_param("usps_api_url", usps_api_url)
        param.set_param("usps_username", usps_username)
        param.set_param("usps_password", usps_password)
