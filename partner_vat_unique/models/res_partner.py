# Copyright 2017 Grant Thornton Spain - Ismael Calvo <ismael.calvo@es.gt.com>
# Copyright 2020 Manuel Calero - Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import config


class ResPartner(models.Model):
    _inherit = "res.partner"

    vat = fields.Char(copy=False)

    @api.constrains("vat")
    def _check_vat_unique(self):
        for record in self:
            if record.parent_id or not record.vat:
                continue
            test_condition = config["test_enable"] and not self.env.context.get(
                "test_vat"
            )
            if test_condition:
                continue
            if record.same_vat_partner_id:
                raise ValidationError(
                    _("The VAT %s already exists in another partner.") % record.vat
                )
