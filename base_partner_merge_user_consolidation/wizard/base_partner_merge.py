# Copyright 2025 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class MergePartnerAutomatic(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    def _merge(self, partner_ids, dst_partner=None, extra_checks=True):
        """Merge partners, consolidating any multiple user accounts first.

        In 18.0 super()._merge() rejects merges where more than one user
        exists across the partners being merged. We pre-consolidate: groups
        are unioned into the kept user, losing users are archived, and their
        partner_id is temporarily parked on a throwaway partner so super()'s
        guard sees ≤ 1 user across the merge set. The throwaway is deleted
        after super()
        """
        Partner = self.env["res.partner"]
        partner_ids_rs = Partner.browse(partner_ids).exists()
        if not partner_ids_rs or len(partner_ids_rs) < 2:
            return super()._merge(
                partner_ids, dst_partner=dst_partner, extra_checks=extra_checks
            )
        if dst_partner and dst_partner.exists() and dst_partner in partner_ids_rs:
            final_partner = dst_partner
        else:
            final_partner = self._get_ordered_partner(partner_ids_rs.ids)[-1]
        Users = self.env["res.users"].sudo().with_context(active_test=False)
        all_users = Users.search([("partner_id", "in", partner_ids_rs.ids)])
        parking_partner = None
        if len(all_users) > 1:
            kept_user, losing_users = self._pick_kept_user(all_users)
            self._union_user_groups(kept_user, losing_users)
            self._archive_users(losing_users)
            kept_user.write({"partner_id": final_partner.id})
            # Park losing users on a throwaway partner so super()'s
            # active_test=False user-count guard sees only kept_user.
            # res_users.partner_id is NOT NULL so we can't set it to False.
            parking_partner = Partner.sudo().create({"name": "__merge_parking__"})
            self.env.cr.execute(
                "UPDATE res_users SET partner_id = %s WHERE id = ANY(%s)",
                (parking_partner.id, losing_users.ids),
            )
            self.env.invalidate_all()
        try:
            return super()._merge(
                partner_ids, dst_partner=dst_partner, extra_checks=extra_checks
            )
        finally:
            if parking_partner:
                # Move parked users to final_partner before deleting parking
                self.env.cr.execute(
                    "UPDATE res_users SET partner_id = %s WHERE partner_id = %s",
                    (final_partner.id, parking_partner.id),
                )
                self.env.invalidate_all()
                parking_partner.sudo().unlink()

    def _pick_kept_user(self, users):
        """Find user by login_date or create_date."""
        users = users.sorted(key=lambda user: (user.login_date or user.create_date))
        kept = users[-1]
        return kept, (users - kept)

    def _union_user_groups(self, kept_user, losing_users):
        """Union of all groups from obsolete users to kept_user."""
        if not kept_user or not losing_users:
            return
        keep = set(kept_user.groups_id.ids)
        add = set(losing_users.mapped("groups_id").ids) - keep
        if add:
            kept_user.sudo().write({"groups_id": [(4, gid) for gid in add]})

    def _archive_users(self, users):
        """Deactivate obsolete users and scramble their login."""
        for user in users.sudo():
            new_login = f"__merged_user_{user.id}_{user.login or '-'}"
            user.write({"active": False, "login": new_login})
