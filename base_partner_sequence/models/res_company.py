# Copyright 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_ref_readonly = fields.Boolean(
        string="Partner Reference Readonly",
        help="If marked, the Reference in partners will not be editable.",
    )
