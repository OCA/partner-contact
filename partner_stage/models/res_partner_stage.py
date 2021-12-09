# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PartnerStage(models.Model):
    _name = "res.partner.stage"
    _description = "Contact Stage"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    code = fields.Char()
    sequence = fields.Integer(help="Used to order the stages", default=10)
    fold = fields.Boolean()
    active = fields.Boolean(default=True)
    description = fields.Text(translate=True)
    is_default = fields.Boolean("Default state")

    state = fields.Selection(
        [("draft", "To Approve"), ("confirmed", "Approved"), ("cancel", "Archived")],
        string="Related State",
        default="confirmed",
    )

    _sql_constraints = [
        ("res_partner_stage_code_unique", "UNIQUE(code)", "Stage Code must be unique.")
    ]

    @api.constrains("is_default")
    def _check_default(self):
        if self.search_count([("is_default", "=", True)]) > 1:
            raise ValidationError(_("There should be only one default stage"))
