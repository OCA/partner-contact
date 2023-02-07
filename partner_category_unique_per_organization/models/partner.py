# Copyright 2023 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains("category_id")
    def _check_category_unique_per_organization(self):
        for record in self:
            for categ in record.category_id.filtered("unique_per_organization"):
                already_existing_contacts = (
                    record.commercial_partner_id.child_ids.filtered(
                        lambda c: c.id != record.id and categ.id in c.category_id.ids
                    )
                )
                if already_existing_contacts:
                    raise UserError(
                        _(
                            "You can only have 1 contact with the category"
                            " {} in the organization {} ({})"
                        ).format(
                            categ.name,
                            record.commercial_partner_id.name,
                            already_existing_contacts[0].name,
                        )
                    )
