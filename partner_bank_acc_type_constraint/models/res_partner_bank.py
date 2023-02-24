# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    acc_type_manual = fields.Selection(
        selection=lambda self: self.get_supported_account_types(),
        default=lambda self: self._default_acc_type_manual(),
        string="Account Type",
    )
    # The string of acc_type is "Type", but it is never visible in the view

    @api.model
    def _default_acc_type_manual(self):
        sel = self.get_supported_account_types()
        sel_dict = dict(sel)
        if "iban" in sel_dict:
            return "iban"
        elif len(sel) == 1:
            return sel[0][0]
        return False

    @api.constrains("acc_type_manual", "acc_number")
    def _check_acc_type_manual(self):
        for rec in self:
            if rec.acc_type != rec.acc_type_manual:
                acctype2label = dict(
                    rec.fields_get("acc_type_manual", "selection")["acc_type_manual"][
                        "selection"
                    ]
                )
                raise ValidationError(
                    _(
                        "The type of account number '%(acc_number)s' is "
                        "'%(acc_type)s' and not '%(acc_type_manual)s'.",
                        acc_number=rec.acc_number,
                        acc_type=acctype2label.get(rec.acc_type),
                        acc_type_manual=acctype2label.get(rec.acc_type_manual),
                    )
                )
