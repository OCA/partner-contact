# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    supplier_ref = fields.Char(readonly=True)

    def _get_next_supplier_ref(self, vals=None):
        return self.env["ir.sequence"].next_by_code("res.partner.supplier")

    def _needs_supplier_ref(self, vals=None):
        if not vals and not self:
            raise UserError(_("Either field values or an id must be provided."))
        fields_for_check = [
            "is_company",
            "parent_id",
            "is_supplier",
        ]
        if vals:
            vals_for_check = vals.copy()
        else:
            vals_for_check = {}
        if self:
            for field in fields_for_check:
                if field not in vals_for_check:
                    vals_for_check[field] = self[field]
        return vals_for_check.get("is_supplier") and (
            vals_for_check.get("is_company") or not vals_for_check.get("parent_id")
        )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("supplier_ref") and self._needs_supplier_ref(vals=vals):
                vals["supplier_ref"] = self._get_next_supplier_ref(vals=vals)
        return super().create(vals_list)

    def copy(self, default=None):
        default = default or {}
        if self._needs_supplier_ref():
            default["supplier_ref"] = self._get_next_supplier_ref()
        return super().copy(default=default)

    def write(self, vals):
        for partner in self:
            partner_vals = vals.copy()
            if (
                not partner_vals.get("supplier_ref")
                and partner._needs_supplier_ref(vals=partner_vals)
                and not partner.supplier_ref
            ):
                partner_vals["supplier_ref"] = partner._get_next_supplier_ref(
                    vals=partner_vals
                )
            super(ResPartner, partner).write(partner_vals)
        return True
