# Copyright 2023 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    children_notes = fields.One2many("mail.message", compute="_compute_children_notes")

    def _get_children_for_notes(self):
        return self.mapped("child_ids").filtered(lambda c: c.type == "contact")

    def _get_notes_from_children(self):
        subtype_note = self.env.ref("mail.mt_note")
        return self.mapped("message_ids").filtered(
            lambda m: m.message_type == "comment" and m.subtype_id == subtype_note
        )

    @api.depends("child_ids", "child_ids.message_ids")
    def _compute_children_notes(self):
        for record in self:
            children = record._get_children_for_notes()
            record.children_notes = children._get_notes_from_children()
