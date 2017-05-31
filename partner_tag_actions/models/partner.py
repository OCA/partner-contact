# -*- coding: utf-8 -*-
# Copyright 2016 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def count_actions(self):
        for record in self:
            record.action_count = len(record.action_ids)

    action_count = fields.Integer(compute=count_actions)
    action_ids = fields.One2many('partner.action', 'partner_id',
                                 string='Actions')

    @api.multi
    def button_actions(self):
        self.ensure_one()

        return {
            'name': _('Actions'),
            'type': 'ir.actions.act_window',
            'res_model': 'partner.action',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('partner_id', '=', self.id)],
        }

    def apply_actions(self):
        self.ensure_one()
        actions = self.action_ids.filtered(lambda a: a.state == 'done')
        actions = actions.sorted(reverse=True)
        actions.apply_all()
        return True

    @api.multi
    def write(self, vals):
        res = super(Partner, self).write(vals)
        if "category_id" in vals and "norecurse" not in self.env.context:
            self.with_context(norecurse=True).apply_actions()

        return res
