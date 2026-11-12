# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_vat_unique = fields.Boolean(
        string="Unique VAT Constraint",
        config_parameter="partner_vat_unique.partner_vat_unique",
        help="Check this if you want to constrain VAT number to be unique.",
    )
