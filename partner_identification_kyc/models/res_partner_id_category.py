from odoo import fields, models


class ResPartnerIdCategory(models.Model):
    _inherit = "res.partner.id_category"

    is_kyc = fields.Boolean(
        string="Is KYC Category",
        default=False,
        help="Marks this category as the one used for KYC processes. It enables "
        "KYC-specific behaviour such as the automatic identification number "
        "sequence and child-contact handling.",
    )
    enable_on_child_contacts = fields.Boolean(
        string="Enable on Child Contacts",
        default=False,
        help="If checked, KYC checks can be performed on child contacts of a company.",
    )
