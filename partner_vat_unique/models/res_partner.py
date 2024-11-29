# Copyright 2017 Grant Thornton Spain - Ismael Calvo <ismael.calvo@es.gt.com>
# Copyright 2020 Manuel Calero - Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    vat = fields.Char(copy=False)

    @api.constrains("vat", "parent_id")
    def _check_vat_unique(self):
        if (
            not self.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_vat_unique.partner_vat_unique", default=False)
        ):
            return

        for record in self:
            if record.parent_id or not record.vat:
                continue

            if record.same_vat_partner_id:
                raise ValidationError(
                    self.env._(
                        "The VAT %(vat)s already exists in another partner.",
                        vat=record.vat,
                    )
                )
