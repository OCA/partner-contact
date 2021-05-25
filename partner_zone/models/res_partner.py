# Copyright 2021 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    zone_ids = fields.Many2many(
        comodel_name='partner.zone',
        relation='partner_zone_rel',
        column1='partner_id',
        column2='zone_id',
        string='Zones',
    )

    def _prepare_zone_domain(self, domain):
        domain += [
            '&',
            ('child_id', '=', False),
            '|',
            '&',
            '|',
            ('industry_ids', 'in', self.industry_id.ids),
            ('industry_ids', '=', False),
            '|',
            ('category_ids', 'in', self.category_id.ids),
            ('category_ids', '=', False),
            '|',
            '|',
            ('industry_ids', 'in', self.industry_id.ids),
            ('industry_ids', '=', False),
            '|',
            ('category_ids', 'in', self.category_id.ids),
            ('category_ids', '=', False),
        ]

    def _get_possible_zone_criteria(self):
        domain = []
        self._prepare_zone_domain(domain)
        zone_ids = self.env['partner.zone'].search(domain)
        return zone_ids

    def _compute_zone(self):
        zone_ids = self._get_possible_zone_criteria()
        result_ids = self.env['partner.zone']

        result_ids |= zone_ids.filtered(lambda x: (
            self.country_id.id in x.country_ids.ids and
            not x.state_ids and not x.city_ids.ids
        ))
        result_ids |= zone_ids.filtered(
            lambda x: self.state_id.id in x.state_ids.ids and not x.city_ids.ids
        )
        result_ids |= zone_ids.filtered(
            lambda x: self.city_id.id in x.city_ids.ids
        )
        if result_ids:
            self.zone_ids = result_ids

    @api.onchange('country_id', 'state_id', 'city_id', 'category_id', 'industry_id')
    def _onchange_partner_zone(self):
        if not self.name:
            # We wait until the name is filled
            return
        self._compute_zone()

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        if not res.zone_ids:
            res._compute_zone()
        return res

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if not vals.get('zone_ids') and not self.zone_ids:
            self._compute_zone()
        return res
