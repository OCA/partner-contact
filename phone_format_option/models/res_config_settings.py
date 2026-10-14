# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # ``NATIONAL`` and ``INTERNATIONAL`` are the ``force_format`` values expected
    # by ``phone_validation``'s ``_phone_format``, so they can be passed through
    # as-is. ``RAW`` is handled by this module and means no reformatting.
    phone_format = fields.Selection(
        [
            ("RAW", "As entered (no formatting)"),
            ("NATIONAL", "National (without country code)"),
            ("INTERNATIONAL", "International (with country code)"),
        ],
        default="INTERNATIONAL",
        required=True,
        config_parameter="phone_format_option.phone_format",
        help="Format applied to the phone and mobile numbers of contacts. "
        "When set to National, contacts located in a different country from "
        "your company are still formatted in international format.",
    )
