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

    @api.model
    def _get_vies_data(self, vat, raise_if_fail=False):
        res = {}
        try:
            result = check_vies(vat)
        except Exception as e:
            _logger.warning("Failed to query VIES: %s" % e)
            if raise_if_fail:
                raise UserError(_("Failed to query VIES.\nTechnical error: %s.") % e)
            return res
        if result.valid and result.name:
            res["vat"] = vat
            # Update partner name if listed on VIES
            if result.name != "---":
                res["name"] = result.name.upper()
            # Update partner address if listed on VIES
            if result.address != "---":
                res["street"] = (
                    result.address.replace("\n", " ").replace("\r", "").title()
                )
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
                    partner.update(result)
