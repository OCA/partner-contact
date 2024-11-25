# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, exceptions, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    industry_id = fields.Many2one(string="Main Industry")

    secondary_industry_ids = fields.Many2many(
        comodel_name="res.partner.industry",
        string="Secondary Industries",
        domain="[('id', '!=', industry_id)]",
    )

    show_partner_industry_for_person = fields.Boolean(
        compute="_compute_show_partner_industry_for_person",
    )

    def _compute_show_partner_industry_for_person(self):
        for partner in self:
            partner.show_partner_industry_for_person = self.env.user.has_group(
                "partner_industry_secondary" ".group_use_partner_industry_for_person"
            )

    @api.constrains("industry_id", "secondary_industry_ids")
    def _check_industries(self):
        for partner in self:
            if partner.industry_id in partner.secondary_industry_ids:
                raise exceptions.ValidationError(
                    self.env._(
                        "The main industry must be different "
                        "from the secondary industries."
                    )
                )
