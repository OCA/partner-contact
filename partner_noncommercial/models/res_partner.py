# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    parent_id = fields.Many2one(string="Related organization")
    user_id = fields.Many2one(string="Responsible")
    company_type = fields.Selection(
        selection_add=[("company", "Organization")], string="Organization Type"
    )
