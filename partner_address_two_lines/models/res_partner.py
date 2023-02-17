# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_contact_name(self, partner, name):
        if self.env.context.get("_two_lines_partner_address"):
            return "{}\n {}".format(
                partner.commercial_company_name or partner.sudo().parent_id.name, name
            )
        else:
            return super()._get_contact_name(partner, name)
