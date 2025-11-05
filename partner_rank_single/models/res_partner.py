# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import ValidationError


class Contact(models.Model):
    _inherit = "res.partner"

    @api.constrains("customer_rank", "supplier_rank")
    def _constrains_single_rank(self):
        for record in self:
            if record.customer_rank > 0 and record.supplier_rank > 0:
                raise ValidationError(
                    self.env._("A contact cannot be both a customer and a supplier.")
                )

    def _increase_rank(self, field, n=1):
        # OVERRIDE: to check single rank
        # Because of direct SQL update in the super method
        res = super()._increase_rank(field, n=n)
        self._constrains_single_rank()
        return res
