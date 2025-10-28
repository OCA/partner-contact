# Copyright 2025 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class MergePartnerAutomatic(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    def _merge(self, partner_ids, dst_partner=None, extra_checks=True):
        """Merge partners, assign a single user"""
        super()._merge(partner_ids, dst_partner=dst_partner, extra_checks=extra_checks)
        # Recompute dst_partner
        Partner = self.env["res.partner"]
        partner_ids_rs = Partner.browse(partner_ids).exists()
        if not partner_ids_rs or len(partner_ids_rs) < 1:
            return
        if dst_partner and dst_partner.exists():
            final_partner = dst_partner
        else:
            final_partner = self._get_ordered_partner(partner_ids_rs.ids)[-1]
        # Find all users for final partner
        Users = self.env["res.users"].sudo()
        partner_users = Users.search([("partner_id", "=", final_partner.id)])
        if len(partner_users) <= 1:
            return
        kept_user, losing_users = self._pick_kept_user(partner_users)
        # Link and make sure that user is active
        kept_user.write(
            {
                "partner_id": final_partner.id,
                "active": True,
            }
        )
        # Merge all groups from all users to final user
        self._union_user_groups(kept_user, losing_users)
        # Deactivate remaining users
        self._archive_users(losing_users)

    def _pick_kept_user(self, users):
        """Find user by login_date or create_date"""
        users = users.sorted(key=lambda user: (user.login_date or user.create_date))
        kept = users[-1]
        return kept, (users - kept)

    def _union_user_groups(self, kept_user, losing_users):
        """Union of all groups from obsolete users, to kept_user"""
        if not kept_user or not losing_users:
            return
        keep = set(kept_user.groups_id.ids)
        add = set(losing_users.mapped("groups_id").ids) - keep
        if add:
            # implied_ids and trans_implied_ids are taken care of here
            # https://github.com/OCA/OCB/blob/16.0/odoo/addons/base/models/res_users.py#L1403
            kept_user.sudo().write({"groups_id": [(4, gid) for gid in add]})

    def _archive_users(self, users):
        """Deactivate obsolete users, scramble login"""
        for user in users.sudo():
            new_login = f"__merged_user_{user.id}_{user.login or '-'}"
            user.write(
                {
                    "active": False,
                    "login": new_login or user.login,
                }
            )
