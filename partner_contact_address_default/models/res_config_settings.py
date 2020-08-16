from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_address_default_allow_all_partner = fields.Boolean(
        'Allow selecting from all partners as address default',
        help='Allow selecting from all partners as address default',
        implied_group='partner_contact_address_default.group_allow_all_partner',
        default=False,
    )
