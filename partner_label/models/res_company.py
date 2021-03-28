# Copyright 2017-2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_labels_width = fields.Float(
        "Width",
        default=60,
        help="Width in millimeters",
        required=True,
    )
    partner_labels_height = fields.Float(
        "Height",
        default=42.3,
        help="Height in millimeters",
        required=True,
    )
    partner_labels_padding = fields.Float(
        "Padding",
        default=5,
        help="Padding in millimeters",
        required=True,
    )
    partner_labels_margin_top = fields.Float(
        string="Margin Top",
        default=1,
        help="Margin top in millimeters",
        required=True,
    )
    partner_labels_margin_bottom = fields.Float(
        string="Margin Bottom",
        default=1,
        help="Margin bottom in millimeters",
        required=True,
    )
    partner_labels_margin_left = fields.Float(
        string="Margin Left",
        default=1,
        help="Margin left in millimeters",
        required=True,
    )
    partner_labels_margin_right = fields.Float(
        string="Margin Right",
        default=1,
        help="Margin right in millimeters",
        required=True,
    )
