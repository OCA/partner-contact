#  -*- coding: utf-8 -*-
#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class Company(models.Model):
    _inherit = 'res.company'

    name = fields.Char(translate=True)
    lang = fields.Selection(
        related='partner_id.lang',
        string='Language',
        help="If the selected language is loaded in the system, "
             "all documents related to this contact will be printed in this language. If not, it will be English.")
    street = fields.Char(translate=True)
    street2 = fields.Char(translate=True)
    city = fields.Char(translate=True)

    def address_name_translate(self, name):
        return name

    def _force_address(self, vals):
        company = self.with_context(dict(self._context, lang='en_US'))
        lang_name = f'display_name_{self.env.user.lang.split("_")[0]}'
        if lang_name in self._fields:
            if vals.get('city'):
                company.city = self.address_name_translate(vals['city'])
            if vals.get('street'):
                company.street = self.address_name_translate(vals['street'])

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)
        for company, vals in zip(companies, vals_list):
            company._force_address(vals)
        return companies

    def write(self, vals):
        res = super().write(vals)
        if vals.get('street') or vals.get('city'):
            for company in self:
                company._force_address(vals)
        return res
