# Copyright 2025 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _has_propagating_relations(self):
        """Return True if partner has at least one relation with propagate_archive=True."""
        self.ensure_one()
        Relation = self.env["res.partner.relation"].sudo()
        return bool(
            Relation.search_count(
                [
                    "|",
                    ("left_partner_id", "=", self.id),
                    ("right_partner_id", "=", self.id),
                    ("type_id.propagate_archive", "=", True),
                ]
            )
        )

    def _get_archive_propagation_candidates(self):
        """Extend archive propagation candidates with propagating relations for companies"""
        self.ensure_one()
        res = super()._get_archive_propagation_candidates()
        if self.is_company:
            res |= self._get_related_partners_for_archive_propagation()
        return res - self

    def _compute_show_prop_wizard_button(self):
        # Keep original logic (children) and extend for relation-based propagation.
        res = super()._compute_show_prop_wizard_button()
        for partner in self:
            if partner.is_company and partner._has_propagating_relations():
                partner.show_prop_wizard_button = True
        return res

    def _get_related_partners_for_archive_propagation(self):
        """Return partners related to self via types with propagate_archive."""
        self.ensure_one()
        Relation = self.env["res.partner.relation"].sudo()
        relations = Relation.search(
            [
                "|",
                ("left_partner_id", "=", self.id),
                ("right_partner_id", "=", self.id),
                ("type_id.propagate_archive", "=", True),
            ]
        )
        related = self.env["res.partner"]
        for rel in relations:
            if rel.left_partner_id == self:
                other = rel.right_partner_id
            else:
                other = rel.left_partner_id
            related |= other
        return related

    def _archive_propagate_wizard(self):
        """
        Only organisational partners (is_company = True) propagate via relations.
        -On archive: related partners (via relation types with propagate_archive = True)
          are archived when possible and flagged with propagated_from_id = source company.
        """
        res = super()._archive_propagate_wizard()
        self._archive_multi_relation()
        return res

    def _archive_propagate_external(self):
        res = super()._archive_propagate_external()
        self._archive_multi_relation()
        return res

    def _archive_multi_relation(self):
        companies = self.filtered(lambda p: p.is_company)
        if not companies:
            return
        for company in companies:
            related = company._get_related_partners_for_archive_propagation().filtered(
                lambda p: p.active
            )
            if not related:
                continue
            archivable, unarchivable = related._split_archivable_unarchivable_user()
            archivable.write(
                {
                    "active": False,
                    "propagated_from_id": company.id,
                }
            )
            company._notify_skipped_partners(unarchivable)
