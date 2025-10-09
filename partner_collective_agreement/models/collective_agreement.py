# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CollectiveAgreement(models.Model):
    _name = "collective.agreement"
    _description = "Collective Agreement"
    _check_company_auto = True

    code = fields.Char(required=True)
    name = fields.Text(required=True)
    scope_id = fields.Many2one(
        "collective.agreement.scope", string="Scope", required=True
    )
    publication_date = fields.Date(required=True)
    end_date = fields.Date()
    official_publication_id = fields.Many2one(
        "collective.agreement.official.publication",
        string="Official Publication",
        required=True,
    )
    observations = fields.Text()
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("finished", "Finished"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        required=True,
    )
    active = fields.Boolean(default=True)
    partner_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="collective_agreement_partner_rel",
        column1="agreement_id",
        column2="partner_id",
        string="Partners",
        check_company=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    _sql_constraints = [
        ("code_uniq", "unique(code)", "The code must be unique"),
        ("name_uniq", "unique(name)", "The name must be unique"),
    ]

    @api.constrains("end_date", "publication_date")
    def _check_end_date(self):
        for record in self:
            if record.end_date and record.end_date < record.publication_date:
                raise ValidationError(
                    _("The end date cannot be earlier than the publication date.")
                )
