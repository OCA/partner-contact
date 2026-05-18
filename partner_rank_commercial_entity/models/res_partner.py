# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Contact(models.Model):
    _inherit = "res.partner"

    @api.model
    def _commercial_fields(self):
        return super()._commercial_fields() + ["customer_rank", "supplier_rank"]

    def _increase_rank(self, field, n=1):
        # OVERRIDE: to update ranks only on commercial entity level
        if field in ("customer_rank", "supplier_rank"):
            res = super(Contact, self.commercial_partner_id)._increase_rank(field, n=n)
            # The ``res.partner::_increase_rank`` method updates the rank
            # executing a direct sql update query, so bypass ORM mechanisms.
            # Therefore, we need to manually sync the updated rank to children.
            self.sudo()._commercial_sync_to_children(["customer_rank", "supplier_rank"])
            return res
        return super()._increase_rank(field, n=n)
