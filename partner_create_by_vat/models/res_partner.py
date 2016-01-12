# -*- coding: utf-8 -*-
# ©  2015 Forest and Biomass Services Romania
# See README.rst file on addons root folder for license details

from openerp import models, api, _
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_partner_data(self, vat):
        try:
            from stdnum.eu.vat import check_vies
        except:
            ValidationError(_('Error!'),
                            _("There was an error importing check_vies "
                              "method from python stdnum."))
        res = {}
        vat = vat.strip().upper()
        vat_country, vat_number = self._split_vat(vat)
        result = check_vies(vat)
        # Check if partner is listed on Vies
        if result.name is not None:
            # Check is the partner have the name and adress listed on VIES
            if result.name != '---':
                # Get country by country code
                country = self.env['res.country'].search(
                    [('code', 'ilike', vat_country)])
                new_name = result.name.upper()
                if result.address != '---':
                    new_address = result.address.replace(
                        '\n', ' ').replace('\r', '').title()
                res.update({
                    'name': new_name,
                    'vat': vat,
                    'street': new_address,
                    'country_id': country and country[0].id,
                    'vat_subjected':  result.valid
                })
            else:
                res['vat_subjected'] = result.valid
                raise ValidationError(_("The partner doesn't have the name "
                                        "and address listed on Vies "
                                        "Webservice."))
        else:
            raise ValidationError(_("The partner is not listed on Vies "
                                    "Webservice."))
        return res

    @api.multi
    def vat_change(self, value):
        res = super(ResPartner, self).vat_change(value)
        # Update fields with the values available in the upper method
        # Skip required name error
        with self.env.do_in_onchange():
            if value:
                result = self._get_partner_data(value)
                res['value'].update(result)
        return res

    @api.one
    def get_partner_data(self):
        res = self._get_partner_data(self.vat)
        self.update(res)
