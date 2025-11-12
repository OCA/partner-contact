# Copyright 2025 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class ArchivePropagateWizard(models.TransientModel):
    _name = "res.partner.archive.propagate.wizard"
    _description = "Archive partner and children of partner "

    partner_id = fields.Many2one("res.partner", required=True, readonly=True)
    line_ids = fields.One2many(
        "res.partner.archive.propagate.line", "wizard_id", string="Contacts to archive"
    )

    def action_confirm(self):
        """Archive main partner from the ui:
        - silently archive NON-contact type descendants (invoice/delivery/etc)
        - skip descendants linked to active users and notify
        """
        self.ensure_one()
        self.partner_id.with_context(partner_archive_propagate_ui=True).write(
            {"active": False}
        )
        partners = (
            self.line_ids.mapped("partner_id").sudo().filtered(lambda p: p.active)
        )
        archivable, unarchivable = partners._split_archivable_unarchivable_user()
        archivable.write(
            {
                "active": False,
                "propagated_from_id": self.partner_id.id,
            }
        )
        self.partner_id._notify_skipped_partners(unarchivable)
        if unarchivable:
            # return a nice message on ui too
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Some contacts were skipped"),
                    "message": _("Skipped contacts linked to active users: %s")
                    % ", ".join(unarchivable.mapped("name")),
                    "type": "warning",
                    "sticky": False,
                },
            }
        return {"type": "ir.actions.act_window_close"}


class ArchiveLine(models.TransientModel):
    _name = "res.partner.archive.propagate.line"
    _description = "Partner Archive Propagate Line"

    wizard_id = fields.Many2one(
        "res.partner.archive.propagate.wizard",
        required=True,
        ondelete="cascade",
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Contact")
    name = fields.Char(related="partner_id.name")
    email = fields.Char(related="partner_id.email")
    phone = fields.Char(related="partner_id.phone")
