# Copyright 2023 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    convert_lastnames_to_uppercase = fields.Boolean(
        default=False,
        config_parameter="partner_lastname_uppercase.convert_lastnames_to_uppercase",
    )
