# Copyright 2025 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    propagated_from_id = fields.Many2one(
        "res.partner",
        string="Archived Due To",
        index=True,
        help=(
            "Technical field. Set when this partner was archived automatically "
            "because the source partner was archived. "
            "Cleared again when it is unarchived by the opposite propagation."
        ),
    )

    show_prop_wizard_button = fields.Boolean(
        compute="_compute_show_prop_wizard_button",
        help="Show or hide the wizard button, depending on child_ids",
    )

    def _compute_show_prop_wizard_button(self):
        for partner in self:
            partner.show_prop_wizard_button = bool(partner.child_ids)

    def write(self, vals):
        """Enable (un)archiving propagation:
        - detect which partners are being (un)archived
        - calls _(un)archive_propagate() on them.
        """
        archiving_partners = self.browse()
        unarchiving_partners = self.browse()
        if "active" in vals:
            if vals["active"] is False:
                archiving_partners = self.filtered(lambda self: self.active)
            elif vals["active"] is True:
                unarchiving_partners = self.filtered(lambda self: not self.active)
        res = super().write(vals)
        from_wizard = self.env.context.get("partner_archive_propagate_ui")
        non_ui = self._force_non_ui()
        # Archiving
        if archiving_partners:
            if from_wizard:
                archiving_partners._archive_propagate_wizard()
            elif non_ui:
                archiving_partners._archive_propagate_external()
        # Unarchiving, always propagate
        if unarchiving_partners:
            unarchiving_partners._unarchive_propagate()
        return res

    def _archive_propagate_wizard(self):
        """Archive descendants according to propagation rules."""
        # Wizard: only non-contact descendants are silently archived here.
        for partner in self:
            non_contacts = (
                partner._get_descendants()
                .sudo()
                .filtered(lambda p: p.active and p.type != "contact")
            )
            if not non_contacts:
                continue
            (
                archivable,
                unarchivable,
            ) = non_contacts._split_archivable_unarchivable_user()
            archivable.write(
                {
                    "active": False,
                    "propagated_from_id": partner.id,
                }
            )
            partner._notify_skipped_partners(unarchivable)

    def _archive_propagate_external(self):
        """Archive descendants according to propagation rules."""
        # Non-UI: archive all children
        for partner in self:
            descendants = partner._get_descendants().sudo().filtered(lambda p: p.active)
            if not descendants:
                continue
            (
                archivable,
                unarchivable,
            ) = descendants._split_archivable_unarchivable_user()
            archivable.write(
                {
                    "active": False,
                    "propagated_from_id": partner.id,
                }
            )
            partner._notify_skipped_partners(unarchivable)

    def _unarchive_propagate(self):
        """Unarchive descendants archived via propagation.
        Only touches partners where propagated_from_id points to the unarchived
        parent, and that are currently inactive.
        """
        to_unarchive = (
            self.env["res.partner"]
            .with_context(active_test=False)
            .sudo()
            .search(
                [
                    ("propagated_from_id", "in", self.ids),
                    ("active", "=", False),
                ]
            )
        )
        if not to_unarchive:
            return
        to_unarchive.write(
            {
                "active": True,
                "propagated_from_id": False,
            }
        )

    def _get_descendants(self):
        """Return only active children."""
        self.ensure_one()
        return self.env["res.partner"].search(
            [("id", "child_of", self.ids), ("id", "!=", self.id)]
        )

    def _split_archivable_unarchivable_user(self):
        """Find which partners are archivable (i.e., no active users) and unarchivable."""
        archivable = self.browse()
        unarchivable = self.browse()
        for partner in self:
            if partner.sudo().user_ids.filtered(lambda u: u.active):
                unarchivable |= partner
                continue
            archivable |= partner
        return archivable, unarchivable

    def _notify_skipped_partners(self, unarchivable_partners):
        """Message listing partners skipped due to active users."""
        unarchivable_partners = unarchivable_partners or self.browse()
        if not unarchivable_partners:
            return
        self.message_post(
            body=_(
                "Skipped archiving the following contacts "
                "because they are linked to active users: %s"
            )
            % ", ".join(unarchivable_partners.mapped("name"))
        )

    @api.model
    def _force_non_ui(self):
        """Read system setting controlling external propagation."""
        return self.env["ir.config_parameter"].sudo().get_param(
            "partner_archive_propagate.force_outside_ui", default="0"
        ) in ("1", "true", "True")

    def action_archive_with_contacts(self):
        """Show wizard only if there are type contact descendants.

        - If there are no type contact descendants: archive immediately.
        - If there are type contact descendants: open wizard listing only those,
          allowing the user to exclude some.
        """
        self.ensure_one()
        descendants = self._get_descendants().filtered(lambda p: p.active)
        contact_desc = descendants.filtered(lambda p: p.type == "contact")
        if not contact_desc:
            # No wizard window opens, archive right away
            return self.with_context(partner_archive_propagate_ui=True).write(
                {"active": False}
            )
        archivable, unarchivable = contact_desc._split_archivable_unarchivable_user()
        wiz = self.env["res.partner.archive.propagate.wizard"].create(
            {
                "partner_id": self.id,
                "line_ids": [(0, 0, {"partner_id": p.id}) for p in archivable],
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": _("Archive Contacts"),
            "res_model": "res.partner.archive.propagate.wizard",
            "view_mode": "form",
            "target": "new",
            "res_id": wiz.id,
        }
