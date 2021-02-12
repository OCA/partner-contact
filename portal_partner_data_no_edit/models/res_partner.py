# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    block_portal_data_edit = fields.Boolean(
        string="Block Customer Info Edit",
        help="Block portal info editing for the portal " "user linked to this partner",
    )
