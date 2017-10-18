# Copyright 2016 Nicolas Bessi, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    city_id = fields.Many2one(
        'res.city',
        compute='_compute_address',
        inverse='_inverse_city_id',
        string="City"
    )
    zip_id = fields.Many2one(
        'res.better.zip',
        string='ZIP Location',
        compute='_compute_address',
        inverse='_inverse_zip_id',
        oldname="better_zip_id",
        help='Use the city name or the zip code to search the location',
    )
    # In order to keep the same logic used in odoo, fields must be computed
    # and inversed, not related. This way, we can ensure that it works
    # correctly on changes and inconsistencies cannot happen.
    # When you make the fields related, the constrains added in res.partner
    # will fail. because when you change the city_id in the company, you are
    # effectively changing it in the partner. The constrains on the partner
    # are evaluated before the inverse methods update the other fields (city,
    # etc..). And we need constrains in the partner to ensure consistency.
    # So, as a conclusion, address fields are very related to each other.
    # Either you make them all related to the partner in company, or you
    # don't for all of them. But mixing methods produces inconsistencies.

    country_enforce_cities = fields.Boolean(
        related='country_id.enforce_cities'
    )

    def _get_company_address_fields(self, partner):
        res = super(ResCompany, self)._get_company_address_fields(partner)
        res['city_id'] = partner.city_id
        res['zip_id'] = partner.zip_id
        return res

    def _inverse_city_id(self):
        for company in self:
            company.partner_id.city_id = company.city_id

    def _inverse_zip_id(self):
        for company in self:
            company.partner_id.zip_id = company.zip_id

    @api.onchange('zip_id')
    def _onchange_zip_id(self):
        if self.zip_id:
            self.zip = self.zip_id.name
            self.city_id = self.zip_id.city_id
            self.city = self.zip_id.city
            self.country_id = self.zip_id.country_id
            if self.country_id.enforce_cities:
                self.state_id = self.city_id.state_id
            else:
                self.state_id = self.zip_id.state_id
