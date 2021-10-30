# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    same_email_partner_id = fields.Many2one(
        "res.partner",
        compute="_compute_same_email_partner_id",
        string="Partner with same e-mail",
        compute_sudo=True,
    )

    @api.depends("email", "company_id")
    def _compute_same_email_partner_id(self):
        for partner in self:
            same_email_partner_id = False
            if partner.email and partner.email.strip():
                partner_email = partner.email.strip().lower()
                domain = [("email", "=ilike", "%" + partner_email + "%")]
                if partner.company_id:
                    domain += [
                        "|",
                        ("company_id", "=", False),
                        ("company_id", "=", partner.company_id.id),
                    ]
                partner_id = partner._origin.id
                if partner_id:
                    domain += [
                        ("id", "!=", partner_id),
                        "!",
                        ("id", "child_of", partner_id),
                        "!",
                        ("id", "parent_of", partner_id),
                    ]
                search_partners = self.with_context(active_test=False).search(domain)
                for search_partner in search_partners:
                    if (
                        search_partner.email
                        and search_partner.email.strip().lower() == partner_email
                    ):
                        same_email_partner_id = search_partner
                        break
            partner.same_email_partner_id = same_email_partner_id
