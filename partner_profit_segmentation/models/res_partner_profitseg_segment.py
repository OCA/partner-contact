# -*- coding: utf-8 -*-
# © 2015 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import Warning


class ResPartnerProfitsegSegment(models.Model):
    _name = 'res.partner.profitseg.segment'
    _description = 'Customer profit segment'

    name = fields.Char(string="Segment name", size=50, required=True)
    lower_limit = fields.Float(string='Lower limit', required=True)
    upper_limit = fields.Float(string='Upper limit', required=True)
    notes = fields.Text('Additional Information')

    _sql_constraints = [
        ('profit_limit_consistency', 'CHECK(lower_limit < upper_limit)',
         'The lower limit must be lower than the upper one!'),
        ('profit_lower_limit_positive', 'CHECK(lower_limit >= 0)',
         'The limit must be positive or zero'),
        ('profit_upper_limit_positive', 'CHECK(upper_limit >= 0)',
         'The limit must be positive or zero')
    ]

    def _check_overlap(self, vals, previous_upper=None, previous_lower=None):
        if vals.get('lower_limit', False) and vals.get('upper_limit', False):
            if self.search([
                '&', '|', '&', ('upper_limit', '>', vals.get('lower_limit')),
                ('lower_limit', '<=', vals.get('upper_limit')),
                '&', ('lower_limit', '<=', vals.get('upper_limit')),
                ('upper_limit', '>=', vals.get('lower_limit')),
                ('id', '!=', self.id)
            ]):
                raise Warning(_('The segment may not overlap with another.'))
        elif vals.get('lower_limit', False):
            segments = self.search([('upper_limit', '<=', previous_lower)])
            uppers = [segment.upper_limit for segment in segments]
            if uppers and vals.get('lower_limit', False) <= max(uppers):
                raise Warning(_('The segment may not overlap with another.'))
        elif vals.get('upper_limit', False):
            segments = self.search([('lower_limit', '>=', previous_upper)])
            lowers = [segment.lower_limit for segment in segments]
            if lowers and vals.get('upper_limit', False) >= min(lowers):
                raise Warning(_('The segment may not overlap with another.'))
        return True

    @api.multi
    def write(self, vals):
        self._check_overlap(
            vals,
            previous_upper=self.upper_limit,
            previous_lower=self.lower_limit)
        return super(ResPartnerProfitsegSegment, self).write(vals)

    @api.model
    def create(self, vals):
        self._check_overlap(vals)
        return super(ResPartnerProfitsegSegment, self).create(vals)
