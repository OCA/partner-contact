# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
import collections


def dict_recursive_update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = dict_recursive_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


class ResPartner(models.Model):
    _inherit = 'res.partner'

    region = fields.Many2one(comodel_name='res.partner.nuts',
                             string="Region")
    substate = fields.Many2one(comodel_name='res.partner.nuts',
                               string="Substate")
    lbl_region = fields.Char(compute='_labels_get')
    lbl_substate = fields.Char(compute='_labels_get')

    @api.one
    @api.depends('country_id')
    def _labels_get(self):
        self.lbl_region = _('Region')
        self.lbl_substate = _('Substate')

    @api.multi
    def onchange_state(self, state_id):
        result = super(ResPartner, self).onchange_state(state_id)
        if not state_id:
            changes = {
                'domain': {
                    'substate': [],
                    'region': [],
                },
                'value': {
                    'substate': False,
                    'region': False,
                }
            }
            dict_recursive_update(result, changes)
        return result

    @api.onchange('substate', 'region')
    def onchange_substate_or_region(self):
        result = {'domain': {}}
        if not self.substate:
            result['domain']['substate'] = []
        if not self.region:
            result['domain']['region'] = []
        return result
