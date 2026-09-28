# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    auto_archive = fields.Boolean(
        help="Archive contact automatically after a period of time", tracking=True
    )

    @api.model
    def _auto_archive_contacts(self):
        contacts_to_archive = self.env["res.partner"].search(
            [("auto_archive", "=", True)]
        )
        contacts_to_archive.action_archive()
        contacts_to_archive.auto_archive = False
