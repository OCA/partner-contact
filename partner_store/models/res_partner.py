# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    type = fields.Selection(selection_add=[("store", "Store Address")])

    def _avatar_get_placeholder_path(self):
        if self.type == "store":
            return "partner_store/static/img/store.png"
        return super()._avatar_get_placeholder_path()
