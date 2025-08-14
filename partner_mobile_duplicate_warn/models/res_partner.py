# Copyright 2021-2022 Akretion France (https://www.akretion.com/).
# Copyright 2025 Therp BV (https://therp.nl/).
# @author: Alexis de Lattre <alexis.delattre@akretion.com>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    same_mobile_partner_id = fields.Many2one(
        "res.partner",
        compute="_compute_same_mobile_partner_id",
        string="Partner with same mobile",
        compute_sudo=True,
    )

    @api.depends(lambda x: x._get_same_mobile_depends())
    def _compute_same_mobile_partner_id(self):
        empty_recordset = self.env[self._name]
        for partner in self:
            partner.same_mobile_partner_id = (
                partner._find_same_mobile_partner()
                if partner.mobile
                else empty_recordset
            )

    def _find_same_mobile_partner(self):
        """Find one partner with the same mobile."""
        self.ensure_one()
        domain = self._get_same_mobile_domain()
        return self.with_context(active_test=False).search(domain, limit=1)

    @api.model
    def _get_same_mobile_depends(self):
        """Return the fields on which same_mobile_partner_id depends.

        Return the fields used in _get_same_mobile_domain function.
        """
        return ["mobile", "company_id"]

    def _get_same_mobile_domain(self):
        """Return domain to find partners with same mobile."""
        self.ensure_one()
        # With phone_validation, the "mobile" field should be
        # clean in E.164 format, without any start/ending spaces
        # So we search on the 'mobile' field with '=' !
        domain = [("mobile", "=", self.mobile)]
        if self.company_id:
            domain += [
                "|",
                ("company_id", "=", False),
                ("company_id", "=", self.company_id.id),
            ]
        self_id = self._origin.id
        if self_id:
            domain.append(("id", "!=", self_id))
        return domain
