# Copyright (C) 2015 Forest and Biomass Romania
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, models
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
        if address and address != "---":
            address_parts = [x for x in address.split("\n") if x]
            if len(address_parts) > 1 and " " in address_parts[-1]:
                # Last line can be "ZipCode City"
                zip_city = address_parts.pop()
                res["zip"], res["city"] = zip_city.split(" ", 1)
            res["street"] = " ".join(address_parts)
        return res

    @api.model
    def _vies_notify(self, notif_type, message):
        bus_send = getattr(self.env.user, "_bus_send", None)
        if bus_send:
            bus_send(
                "simple_notification",
                {
                    "type": notif_type,
                    "title": self.env._("VIES"),
                    "message": message,
                    "sticky": notif_type != "success",
                },
            )

    @api.model
    def _get_vies_data(self, vat, raise_if_fail=False):
        res = {}
        try:
            result = check_vies(vat)
        except Exception as e:
            _logger.warning("Failed to query VIES: %s", e)
            self._vies_notify("danger", self.env._("Failed to query VIES.\n%s", e))
            if raise_if_fail:
                raise UserError(
                    self.env._("Failed to query VIES.\nTechnical error: %s.", e)
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
            self._vies_notify(
                "success",
                self.env._(
                    "VAT %(vat)s validated: %(name)s", vat=vat, name=result.name
                ),
            )
        else:
            self._vies_notify("warning", self.env._("No VIES data found for %s.", vat))
        return res

    def _vies_fetch_result(self):
        self.ensure_one()
        vat = (self.vat or "").strip().upper()
        if not vat or not self.is_company:
            return {}
        vat_country, _vat_number = self._split_vat(vat)
        country = self.country_id
        if vat_country:
            # A country prefix in the VAT wins over the partner's country
            country = (
                self.env["res.country"].search(
                    [("code", "=ilike", vat_country)], limit=1
                )
                or country
            )
        if not country:
            return {}
        try:
            # _run_vat_checks also prefixes unprefixed VATs from EU_PREFIX
            # countries, e.g. a Portuguese '516094564' -> 'PT516094564'
            vat_full, country_code = self._run_vat_checks(
                country, vat, validation="error"
            )
        except ValidationError:
            return {}
        eu_group = self.env.ref("base.europe", raise_if_not_found=False)
        eu_codes = eu_group.country_ids.mapped("code") if eu_group else []
        if not vat_full or (
            country_code not in eu_codes
            and country_code not in EU_EXTRA_VAT_CODES.values()
        ):
            return {}
        return self._get_vies_data(vat_full)

    def _vies_populate(self):
        for partner in self:
            result = partner._vies_fetch_result()
            if result:
                # Context needed for compatibility with
                # partner_country_state_required, and to avoid a recursion
                # through the write override below.
                partner.with_context(
                    no_state_required=True, no_vies_populate=True
                ).write(result)

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        if not self.env.context.get("no_vies_populate"):
            partners._vies_populate()
        return partners

    def write(self, vals):
        res = super().write(vals)
        if "vat" in vals and not self.env.context.get("no_vies_populate"):
            self._vies_populate()
        return res

    @api.onchange("vat")
    def vies_vat_change(self):
        for partner in self:
            result = partner._vies_fetch_result()
            if result:
                # Context needed for compatibility with
                # partner_country_state_required.
                partner.with_context(no_state_required=True).update(result)
