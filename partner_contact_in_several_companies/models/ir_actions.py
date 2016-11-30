# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class IRActionsWindow(models.Model):
    _inherit = 'ir.actions.act_window'

    @api.multi
    def read(self, fields=None, context=None, load='_classic_read'):
        actions = super(IRActionsWindow, self).read(fields=fields, load=load)
        for action in actions:
            if action.get('res_model', '') == u'res.partner':
                # By default, only show standalone contact
                action_context = action.get('context', '{}') or '{}'
                if 'search_show_all_positions' not in action_context:
                    action['context'] = action_context.replace(
                        '{',
                        ("{'search_show_all_positions': "
                         "{'is_set': True, 'set_value': False},"),
                        1)
        return actions

    @api.model
    def _enable_context(self):
        action = self.env.ref('base.action_partner_form')
        if 'search_show_all_positions' not in action.context:

            action_ctx = action.context.replace(
                '{',
                ("{'search_show_all_positions': "
                 "{'is_set': True, 'set_value': False},"),
                1)
            action.write({'context': action_ctx})
        return True
