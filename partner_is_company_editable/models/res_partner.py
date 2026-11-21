# Copyright 2026 Ecosoft Co., Ltd. (https://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_company = fields.Boolean(readonly=False)

    @api.model
    def default_get(self, fields):
        # Standard actions pass default_is_company=True in the context. As the
        # field is now editable, that default would be kept on create and skip
        # the automatic classification.
        res = super().default_get(fields)
        res.pop("is_company", None)
        return res
