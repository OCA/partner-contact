# -*- coding: utf-8 -*-
# ©  2015 Forest and Biomass Services Romania
# See README.rst file on addons root folder for license details

from openerp import models, fields, api, _
from openerp.exceptions import except_orm


class ResPartner(models.Model):
    _inherit = "res.partner"

    name = fields.Char('Name', required=True, select=True, default=' ')

    @api.one
    def check_vat_name(self):
        # If the partner doesn't have the vat field completed, check if the
        # name field is a valid vat number.
        if self.vat:
            return
        elif self.name:
            self.name = self.name.strip().upper()
            try:
                from stdnum.eu.vat import validate
                validate(self.name)
                self.vat = self.name
            except:
                raise except_orm(_('Error!'),
                                 _("VAT number invalid."))
        else:
            raise except_orm(_('Error!'),
                             _("No VAT number inputted."))

    @api.one
    def button_get_partner_data(self):
        if not self.vat:
            self.check_vat_name()
        else:
            self.vat = self.vat.strip().upper()
        vat_country, vat_number = self._split_vat(self.vat)
        # Complete country field based on country code
        self.country_id = self.env['res.country'].search(
            [('code', 'ilike', vat_country)])[0].id
        from stdnum.eu.vat import check_vies
        result = check_vies(self.vat)
        # Check if partner is listed on Vies
        if result.name is not None:
            # Check is the partner have the name and adress listed on VIES
            if result.name != '---':
                new_name = result.name.upper()
                if result.address != '---':
                    new_address = result.address.replace(
                        '\n', ' ').replace('\r', '').title()
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
