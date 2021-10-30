# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    same_mobile_partner_id = fields.Many2one(
        "res.partner",
        compute="_compute_same_mobile_partner_id",
        string="Partner with same mobile",
        compute_sudo=True,
    )

    @api.depends("mobile", "company_id")
    def _compute_same_mobile_partner_id(self):
        # With phone_validation, the "mobile" field should be
        # clean in E.164 format, without any start/ending spaces
        # So we search on the 'mobile' field with '=' !
        for partner in self:
            same_mobile_partner_id = False
            if partner.mobile:
                domain = [("mobile", "=", partner.mobile)]
                if partner.company_id:
                    domain += [
                        "|",
                        ("company_id", "=", False),
                        ("company_id", "=", partner.company_id.id),
                    ]
                partner_id = partner._origin.id
                if partner_id:
                    domain.append(("id", "!=", partner_id))
                same_mobile_partner = self.with_context(active_test=False).search(
                    domain, limit=1
                )
                same_mobile_partner_id = same_mobile_partner.id or False
            partner.same_mobile_partner_id = same_mobile_partner_id
