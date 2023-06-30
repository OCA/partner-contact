# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_contact_name(self, partner, name):
        if self.env.context.get("_two_lines_partner_address"):
            company_name = (
                partner.commercial_company_name or partner.sudo().parent_id.name
            )
            # Depends on https://github.com/odoo/odoo/pull/126451
            # This change can only be merged after this Odoo PR is merged as well.
            if company_name and name:
                # Only display two lines if both values are found.
                return "{}\n{}".format(company_name, name)
        return super()._get_contact_name(partner, name)
