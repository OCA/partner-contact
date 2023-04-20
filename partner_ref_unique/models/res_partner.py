# Copyright 2016 Antonio Espinosa
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains("ref", "is_company", "company_id")
    def _check_ref(self):
        # if base_partner_sequence is installed, ref will be copied to child contacts
        # In that case, don't check child contacts when looking for duplicates
        ref_copied_to_child = "ref" in self._commercial_fields()
        for partner in self.filtered("ref"):
            if ref_copied_to_child and partner.parent_id:
                # Don't check duplicates for child records
                continue
            # If the company is not defined in the partner, take current user company
            company = partner.company_id or self.env.company
            mode = company.partner_ref_unique
            if mode == "all" or (mode == "companies" and partner.is_company):
                domain = [
                    ("id", "!=", partner.id),
                    ("ref", "=", partner.ref),
                ]
                if mode == "companies":
                    domain.append(("is_company", "=", True))
                if ref_copied_to_child:
                    domain.append(("parent_id", "=", False))
                other = self.search(domain)
                # Don't raise when coming from contact merge wizard or no duplicates
                if other and not self.env.context.get("partner_ref_unique_merging"):
                    raise ValidationError(
                        _("This reference is equal to partner '%s'")
                        % other[0].display_name
                    )
