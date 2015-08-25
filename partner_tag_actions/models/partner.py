# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.one
    def count_actions(self):
        self.action_count = len(self.action_ids)

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

    @api.one
    def apply_actions(self):
        actions = self.action_ids.filtered(lambda a: a.state == 'done')
        actions.apply_all()
        return True

    @api.multi
    def write(self, vals):
        res = super(Partner, self).write(vals)
        if "category_id" in vals and "norecurse" not in self.env.context:
            self.with_context(norecurse=True).apply_actions()

        return res
