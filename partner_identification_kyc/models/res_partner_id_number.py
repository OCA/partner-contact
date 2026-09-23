from odoo import api, models


class ResPartnerIdNumber(models.Model):
    _inherit = "res.partner.id_number"

    @api.onchange("category_id")
    def _onchange_category_id_kyc_name(self):
        """Prefill the ID Number from the sequence when the KYC category is set.

        The base ``name`` field is required; for KYC records the number is
        generated automatically so it does not have to be typed when creating
        a record manually through the one2many.
        """
        if self.category_id.is_kyc and not self.name:
            self.name = self.env["ir.sequence"].next_by_code("kyc.identification")

    @api.model_create_multi
    def create(self, vals_list):
        """Auto-assign the identification number from the KYC sequence.

        The base ``name`` field (the ID Number) is required, but for KYC
        records it can be left empty so it gets filled automatically from the
        ``kyc.identification`` sequence, both for the ``Request KYC`` button
        and for records created manually through the one2many.
        """
        for vals in vals_list:
            if vals.get("name"):
                continue
            category = self.env["res.partner.id_category"].browse(
                vals.get("category_id")
            )
            if category.is_kyc:
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("kyc.identification") or "/"
                )
        return super().create(vals_list)
