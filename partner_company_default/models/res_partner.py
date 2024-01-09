# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import config


class ResPartner(models.Model):
    _inherit = "res.partner"

    company_id = fields.Many2one(default=lambda self: self._default_company_id())

    @api.model
    def _default_company_id(self):
        """Return False for other tests or if creating a company."""
        context = self.env.context
        if (
            context.get("creating_from_company")
            or config["test_enable"]
            and not context.get("test_partner_company_default")
        ):
            return False
        return self.env.company
