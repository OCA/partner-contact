# Copyright (C) 2015 Forest and Biomass Romania
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    from stdnum.eu.vat import check_vies
except ImportError:
    _logger.debug("Cannot import check_vies method from python stdnum.")


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _parse_vies_address(self, address):
        res = {}
        if address != "---":
            address_parts = [x for x in address.split("\n") if x]
            if len(address_parts) > 1 and " " in address_parts[-1]:
                # Last line can be "ZipCode City"
                zip_city = address_parts.pop()
                res["zip"], res["city"] = zip_city.split(" ", 1)
            res["street"] = " ".join(address_parts)
        return res

    @api.model
    def _get_vies_data(self, vat, raise_if_fail=False):
        res = {}
        try:
            result = check_vies(vat)
        except Exception as e:
            _logger.warning(f"Failed to query VIES: {e}")
            if raise_if_fail:
                raise UserError(
                    _(f"Failed to query VIES.\nTechnical error: {e}.")
                ) from None
            return res
        _logger.debug(result)
        # Update partner VAT
        if result.valid and result.name:
            res["vat"] = vat
            # Update partner name if listed on VIES
            if result.name != "---":
                res["name"] = result.name.upper()
            # Update partner address if listed on VIES
            res.update(self._parse_vies_address(result.address))
            # Get country by country code
            country = self.env["res.country"].search(
                [("code", "ilike", result.countryCode)]
            )
            if country:
                res["country_id"] = country[0].id
        return res

    @api.onchange("vat")
    def vies_vat_change(self):
        eu_group = self.env.ref("base.europe", raise_if_not_found=False)
        if eu_group:
            for partner in self:
                if not partner.vat or not partner.is_company:
                    continue
                vat = partner.vat.strip().upper()
                vat_country, vat_number = self._split_vat(vat)
                vat_country = vat_country.upper()
                eu_countries = eu_group.country_ids.mapped("code")
                if vat_country and vat_country not in eu_countries:
                    continue
                result = self._get_vies_data(vat)
                if result:
                    # Context needed for compatibility with
                    # partner_country_state_required.
                    partner.with_context(no_state_required=True).update(result)
