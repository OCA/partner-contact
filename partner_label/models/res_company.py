# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    partner_labels_width = fields.Float(
        'Width', default=60, help='Width in millimeters', required=True,
    )
    partner_labels_height = fields.Float(
        'Height', default=42.3, help='Height in millimeters', required=True,
    )
    partner_labels_padding = fields.Float(
        'Padding', default=5, help='Padding in millimeters', required=True,
    )
    partner_labels_margin = fields.Float(
        'Margin', default=1, help='Margin in millimeters', required=True,
    )
