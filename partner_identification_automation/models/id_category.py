from odoo import fields, models


class ResPartnerIdCategory(models.Model):
    _inherit = "res.partner.id_category"

    default_issuer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Default Issuer",
        help="Default issuer for identification numbers of this category",
    )
    default_validity_number = fields.Integer(
        default=1,
        help="Default validity duration number for this category",
    )
    default_validity_unit = fields.Selection(
        [
            ("days", "Days"),
            ("weeks", "Weeks"),
            ("months", "Months"),
            ("years", "Years"),
        ],
        default="years",
        help="Default validity duration unit for this category",
    )

    renewal_lead_number = fields.Integer(
        default=1,
        help='Number of time units before expiry to mark document as "To Renew"',
    )
    renewal_lead_unit = fields.Selection(
        [
            ("days", "Days"),
            ("weeks", "Weeks"),
            ("months", "Months"),
            ("years", "Years"),
        ],
        default="months",
        help="Time unit for renewal lead time",
    )
