# -*- coding: utf-8 -*-
# ©  2015 Forest and Biomass Services Romania
# See README.rst file on addons root folder for license details

from openerp import models, fields, api, _
from openerp.exceptions import except_orm


class ResPartner(models.Model):
    _inherit = "res.partner"

    name = fields.Char('Name', required=True, select=True, default=' ')

    @api.one
    def button_get_partner_data(self):
        # If the partner doesn't have the vat field completed, check if the
        # name field is a valid vat number.
        if not self.vat:
            if self.name and self.name != " ":
                print self.name
                try:
                    name = self.name.strip()
                    print name
                    vat_country, vat_number = self._split_vat(name)
                    print vat_country
                    print vat_number
                    if self.vies_vat_check(vat_country, vat_number):
                        print name.upper()
                        self.vat = name.upper()
                except:
                    raise except_orm(_('Error!'),
                                     _("No valid VAT number found"))

        vat_country, vat_number = self._split_vat(self.vat)
        if vat_number and vat_country:
            self.write({
                'country_id': self.env['res.country'].search(
                    [('code', 'ilike', vat_country)])[0].id
            })
            from stdnum.eu.vat import check_vies
            result = check_vies(self.vat)
            if result.name is not None:
                if result.name != '---':
                    new_name = unicode(result.name).upper()
                    if result.address != '---':
                        new_address = unicode(result.address).title()
                    self.write({
                        'name': new_name,
                        'street': new_address,
                        'vat_subjected':  result.valid
                    })
                else:
                    self.vat_subjected = result.valid
                    raise except_orm(_('Error!'),
                                     _("The partner doesn't have the name and "
                                       "address listed on Vies Webservice."))
            else:
                raise except_orm(_('Error!'),
                                 _("The partner is not listed on Vies "
                                   "Webservice."))
