from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    municipality_id = fields.Many2one(
        'res.country.municipality',
        compute='_compute_address',
        inverse='_inverse_municipality_id',
        domain="[('country_id', '=?', country_id),"
               "('state_id', '=?', state_id)]"
    )

    def _inverse_municipality_id(self):
        for company in self.with_context(skip_check_zip=True):
            company.partner_id.municipality_id = company.municipality_id

    def _get_company_address_field_names(self):
        res = super()._get_company_address_field_names()
        res += ["municipality_id"]
        return res
