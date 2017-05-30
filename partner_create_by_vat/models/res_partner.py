# -*- coding: utf-8 -*-
# ©  2015 Forest and Biomass Services Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

try:
    from stdnum.eu.vat import check_vies
except ImportError:
    _logger.debug("Cannot import check_vies method from python stdnum.")


class ResPartner(models.Model):
    _inherit = "res.partner"

    vat_subjected = fields.Boolean('VAT Legal Statement')

    @api.model
    def _get_vies_data(self):
        res = {}
        vat = self.vat.strip().upper()
        vat_country, vat_number = self._split_vat(vat)
        result = check_vies(vat)
        # Raise error if partner is not listed on Vies
        if result.name is None:
            raise ValidationError(_("The partner is not listed on Vies "
                                    "Webservice."))
        res['vat'] = vat
        res['vat_subjected'] = result.valid
        # Update partner name if listed on VIES
        if result.name != '---':
            res['name'] = result.name.upper()
        # Update partner address if listed on VIES
        if result.address != '---':
            res['street'] = \
                result.address.replace('\n', ' ').replace('\r', '').title()
        # Get country by country code
        country = self.env['res.country'].search(
            [('code', 'ilike', vat_country)])
        if country:
            res['country_id'] = country[0].id
        return res

    @api.onchange('vat')
    def vat_change(self):
        res = {'value': {}}
        # Update fields with the values available in the upper method
        # Skip required name error
        with self.env.do_in_onchange():
            if self.vat:
                result = self._get_vies_data()
                res['value'].update(result)
        return res

    @api.one
    def get_vies_data_from_vat(self):
        if self.vat:
            res = self._get_vies_data()
            self.update(res)
