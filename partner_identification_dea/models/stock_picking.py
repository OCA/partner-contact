# Copyright (C) 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        # Do not allow DO to be completed, if not a valid DEA license.
        for picking in self.filtered(
            lambda p: p.picking_type_code == "outgoing" and p.partner_id
        ):
            running_licenses = picking.partner_id.id_numbers.filtered(
                lambda l: l.status == "open"
                and l.valid_until
                and l.valid_until >= fields.Date.today()
            )
            if not running_licenses:
                raise ValidationError(_("Customer does not have a valid DEA license."))
        return super(StockPicking, self)._action_done()
