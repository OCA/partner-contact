# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _
from odoo.exceptions import MissingError

from odoo.addons.component.core import AbstractComponent


class BasePartnerService(AbstractComponent):
    _inherit = "base.rest.service"
    _name = "base.partner.rest.service"
    _collection = "partner.rest.services"
    _expose_model = None

    def _get(self, _id):
        domain = [("id", "=", _id)]
        record = self.env[self._expose_model].search(domain)
        if not record:
            raise MissingError(
                _("The record %s %s does not exist") % (self._expose_model, _id)
            )
        else:
            return record
