# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PortalWizard(models.TransientModel):
    _inherit = "portal.wizard"

    set_all_users = fields.Boolean(
        string="Invite all the contacts",
        default=False,
    )

    @api.onchange('set_all_users')
    def onchange_set_all_users(self):
        """Toggle between select all partners and the default"""
        if not self.set_all_users:
            for user in self.user_ids:
                user.in_portal = (
                    user.partner_id.user_ids and
                    self.portal_id in user.partner_id.user_ids[0].groups_id
                )
        else:
            not_in_portal = self.user_ids.filtered(lambda x: not x.in_portal)
            not_in_portal.update({'in_portal': True})
