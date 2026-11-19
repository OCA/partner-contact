# Copyright 2026 Canarias Conectada
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_system_admin_contact = fields.Boolean(
        compute="_compute_is_system_admin_contact",
        store=True,
        help="Technical field: true if this contact is linked to an "
        "internal user holding the Administration / Settings group. Used "
        "by the security rule to keep such accounts hidden from regular "
        "internal users in Contacts.",
    )

    @api.depends("user_ids.group_ids")
    def _compute_is_system_admin_contact(self):
        admin_group = self.env.ref("base.group_system")
        for partner in self:
            partner.is_system_admin_contact = admin_group in partner.user_ids.group_ids
