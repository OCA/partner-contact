# Copyright 2017-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_company_type_id = fields.Many2one(
        comodel_name="res.partner.company.type", string="Legal Form"
    )

    @api.constrains(
        "country_id",
        "state_id",
        "partner_company_type_id",
    )
    def _check_partner_company_type_country_state(self):
        for rec in self:
            if not rec.partner_company_type_id:
                return
            if (
                rec.partner_company_type_id.country_ids
                and rec.country_id not in rec.partner_company_type_id.country_ids
            ):
                raise UserError(
                    _(
                        "You must select a Legal Form from the country "
                        "of the partner address."
                    )
                )
            if (
                rec.partner_company_type_id.state_ids
                and rec.state_id not in rec.partner_company_type_id.state_ids
            ):
                raise UserError(
                    _(
                        "You must select a Legal Form from the state "
                        "of the partner address."
                    )
                )
