# © 2021 Le Filament (<http://www.le-filament.com>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    phone_validation_format = fields.Selection(
        selection=[
            ("E164", "E164"),
            ("INTERNATIONAL", "INTERNATIONAL"),
            ("NATIONAL", "NATIONAL"),
            ("RFC3966", "RFC3966"),
        ],
        string="Phone format",
        default="INTERNATIONAL",
        config_parameter="phone_validation_format",
    )

    phone_validation_exception = fields.Boolean(
        string="Raise Exception if incorrect phone number",
        config_parameter="phone_validation_exception",
    )
