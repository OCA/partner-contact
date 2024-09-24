# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)


from odoo import _, api, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _check_setting_block_invoice_address(self):
        partner_block_invoice_address = bool(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_block_invoice_address")
        )
        if not partner_block_invoice_address:
            return False
        partner_block_invoice_address_default_type = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_block_invoice_address_default_type")
        )
        return partner_block_invoice_address_default_type

    @api.onchange("type")
    def _onchange_contact_type(self):
        if self.type == "invoice":
            default_type = self._check_setting_block_invoice_address()
            if default_type:
                self.type = default_type
                return {
                    "warning": {
                        "title": _("Warning"),
                        "message": _(
                            "You cannot set a contact as an invoice address. "
                            "Check the settings."
                        ),
                    },
                }
        return {}

    def write(self, vals):
        if "type" in vals and vals["type"] == "invoice":
            if self._check_setting_block_invoice_address():
                raise UserError(
                    _(
                        "You cannot set a contact as an invoice address. "
                        "Check the settings."
                    )
                )
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if "type" in val and val["type"] == "invoice":
                if self._check_setting_block_invoice_address():
                    raise UserError(
                        _(
                            "You cannot set a contact as an invoice address. "
                            "Check the settings."
                        )
                    )
        return super().create(vals)
