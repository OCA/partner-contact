# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    supplier_ref = fields.Char(
        string="Supplier Reference",
        help="Supplier reference given to this partner.",
        index=True,
        copy=False,
    )

    @api.model
    def _commercial_fields(self):
        """
        Make the supplier reference a field that is propagated
        to the partner's contacts
        """
        return super()._commercial_fields() + [
            "supplier_ref",
        ]
