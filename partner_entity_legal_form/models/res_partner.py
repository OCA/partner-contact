# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    entity_legal_form_id = fields.Many2one(
        "entity.legal.form", string="Entity Legal Form"
    )
    entity_legal_form_abbreviation_id = fields.Many2one(
        "entity.legal.form.abbreviation",
        domain="[('entity_legal_form_id', '=', entity_legal_form_id)]",
        string="Entity Legal Abbreviation",
    )

    @api.constrains(
        "country_id",
        "state_id",
        "entity_legal_form_id",
        "entity_legal_form_abbreviation_id",
    )
    def _check_partner_id_entity_legal_form(self):
        for rec in self:
            if not rec.entity_legal_form_id:
                return
            if rec.country_id and rec.country_id != rec.entity_legal_form_id.country_id:
                raise UserError(
                    _(
                        "You must select a legal entity from the country "
                        "of the partner address."
                    )
                )
            if (
                rec.state_id
                and rec.entity_legal_form_id.state_id
                and rec.state_id != rec.entity_legal_form_id.state_id
            ):
                raise UserError(
                    _(
                        "You must select a legal entity from the state "
                        "of the partner address."
                    )
                )
            if not rec.entity_legal_form_abbreviation_id:
                return
            if (
                rec.entity_legal_form_abbreviation_id.entity_legal_form_id
                != rec.entity_legal_form_id
            ):
                raise UserError(
                    _(
                        "The legal entity abbreviation does not match "
                        "with the legal entity type."
                    )
                )
