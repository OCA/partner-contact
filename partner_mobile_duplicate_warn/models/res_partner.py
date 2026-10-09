# Copyright 2021-2022 Akretion France (https://www.akretion.com/).
# Copyright 2025 Therp BV (https://therp.nl/).
# @author: Alexis de Lattre <alexis.delattre@akretion.com>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # In this version we can only show one duplicate partner at the same time.
    same_mobile_partner_id = fields.Many2one(
        "res.partner",
        compute="_compute_same_mobile_partner_id",
        string="Partner with same mobile",
    )
    same_mobile_count = fields.Integer(
        compute="_compute_same_mobile_partner_id",
        string="Number of partners with the same mobile",
    )
    same_mobile_inaccessible_count = fields.Integer(
        compute="_compute_same_mobile_partner_id",
        string="Partners with same e-mail you cannot access",
    )

    @api.depends(lambda x: x._get_same_mobile_depends())
    def _compute_same_mobile_partner_id(self):
        for partner in self:
            all_matches = partner.sudo()._find_same_mobile_partner()
            accessible_matches = partner._find_same_mobile_partner()  # no sudo
            partner.same_mobile_count = len(all_matches)
            partner.same_mobile_inaccessible_count = partner.same_mobile_count - len(
                accessible_matches
            )
            partner.same_mobile_partner_id = (
                accessible_matches[0]
                if accessible_matches
                else accessible_matches  # the empty recordset
            )

    def _find_same_mobile_partner(self):
        """Find one partner with the same mobile."""
        self.ensure_one()
        domain = self._get_same_mobile_domain()
        return self.with_context(active_test=False).search(domain)

    @api.model
    def _get_same_mobile_depends(self):
        """Return the fields on which same_mobile_partner_id depends.

        Return the fields used in _get_same_mobile_domain function.
        """
        return ["mobile", "company_id"]

    def _get_same_mobile_domain(self, exclude_self=True):
        """Return domain to find partners with same mobile.

        By default we want to find other partners with the
        same mobile, but if we want to see if both self and
        another partner have the same mobile within a domain,
        we will leave out the domain leave that excludes self.

        This can be used to prevent false positives when we want a
        constraint forbidding duplicates.
        """
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
        self_id = (self._origin.id or self.id) if exclude_self else False
        if self_id:
            domain.append(("id", "!=", self_id))
        return domain

    def _find_duplicate_mobile_partner(self):
        """This returns a duplicate partner.

        Duplicate means there is another partner with
        the same mobile and both self and the other partner
        satisfy the search domain.
        """
        self.ensure_one()
        found_partners = self._search_same_mobile_matches_inclusive()
        if self in found_partners and len(found_partners) >= 2:
            other_partners = found_partners - self
            return other_partners[0]
        # Only in extention modules can it happen that self is not
        # found with the domain, for instance when mobile checking
        # should only be done on partners of type 'contact'.
        return self.env[self._name]  # pragma: no cover

    def _search_same_mobile_matches_inclusive(self):
        """Search all records (including self) that satisfy the same-mobile policy."""
        self.ensure_one()
        domain = self._get_same_mobile_domain(exclude_self=False)
        return self.with_context(active_test=False).search(domain)
