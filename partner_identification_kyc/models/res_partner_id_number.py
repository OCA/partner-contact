from odoo import api, fields, models


class ResPartnerIdNumber(models.Model):
    _inherit = "res.partner.id_number"

    category_is_kyc = fields.Boolean(
        string="KYC Category",
        related="category_id.is_kyc",
    )

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
