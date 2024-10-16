# Copyright 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_ref_readonly = fields.Boolean(
        related="company_id.partner_ref_readonly", readonly=False
    )
    # This as general parameter as multi-company behavior is quite impossible
    # to manage correctly as 'ref' field is not company dependent.
    partner_generated_reference_unique = fields.Boolean(
        config_parameter="base_partner_sequence.partner_generated_reference_unique",
        help="Check this if you want to have unique generated references "
        "across all partners (companies, contacts, addresses,...)",
    )
