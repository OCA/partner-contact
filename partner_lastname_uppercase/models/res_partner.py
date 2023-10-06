# Copyright 2023 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _convert_lastnames_to_uppercase(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "partner_lastname_uppercase.convert_lastnames_to_uppercase", False
            )
        )

    @api.model
    def uppercase_all_lastnames(self):
        individuals = self.search(
            [
                ("is_company", "=", False),
                ("lastname", "!=", False),
            ]
        )
        for partner in individuals:
            partner.lastname = partner.lastname.upper()

    @api.model_create_multi
    def create(self, vals_list):
        if self._convert_lastnames_to_uppercase():
            for vals in vals_list:
                is_company = vals.get("is_company", False)
            lastname = vals.get("lastname", False)
            if lastname and not is_company:
                vals["lastname"] = lastname.upper()
        return super().create(vals_list)

    def write(self, vals):
        res = super().write(vals)
        if self._convert_lastnames_to_uppercase():
            # uppercase is done after the write to exclude companies
            if "lastname" in vals or "is_company" in vals:
                individuals = self.filtered(
                    lambda rp: rp.lastname and not rp.is_company
                )
                # looping in case only is_company is in vals (set to false)
                # in that case, uppercase each lastname
                for partner in individuals:
                    super(ResPartner, partner).write(
                        {"lastname": partner.lastname.upper()}
                    )
        return res
