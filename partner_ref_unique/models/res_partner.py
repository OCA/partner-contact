# Copyright 2016 Antonio Espinosa
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains("ref", "is_company", "company_id", "parent_id")
    def _check_ref(self):
        for partner in self.filtered("ref"):
            # If the company is not defined in the partner, take current user company
            company = partner.company_id or self.env.company
            mode = company.partner_ref_unique
            if mode == "none":
                continue
            domain = [
                ("id", "!=", partner.id),
                ("ref", "=", partner.ref),
            ]
            if mode == "exclude_corporative":
                if partner.parent_id:
                    # if reference same as the main on the company skip the check
                    # reference will be checked on company level
                    if partner.ref == partner.parent_id.ref:
                        continue
            if mode == "companies":
                if partner.is_company:
                    domain.append(("is_company", "=", True))
                else:
                    domain.append(("is_company", "=", False))
            other = self.search(domain)
            # Don't raise when coming from contact merge wizard or no duplicates
            if other and not self.env.context.get("partner_ref_unique_merging"):
                raise ValidationError(
                    _("This reference is equal to partner '%s'") % other[0].display_name
                )
