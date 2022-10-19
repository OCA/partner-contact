# Copyright 2022 Ooops Ashish Hirpara  <https://ooops404.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains("mobile")
    def _check_mobile_unique(self):
        if self.env.company.partner_mobile_unique_filter_duplicates:
            for partner in self:
                if partner.mobile:
                    domain = [("mobile", "=", partner.mobile)]
                    if partner.company_id:
                        domain += [
                            "|",
                            ("company_id", "=", False),
                            ("company_id", "=", partner.company_id.id),
                        ]
                    partner_id = partner._origin.id
                    if partner_id:
                        domain += [
                            ("id", "!=", partner.id),
                        ]
                    if self.search(domain):
                        raise UserError(
                            _(
                                "The mobile number is already exists for another partner."
                                " This is not supported when duplicate mobile numbers are "
                                "not allowed."
                            )
                        )
