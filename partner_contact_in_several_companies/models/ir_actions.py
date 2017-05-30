# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class IRActionsWindow(models.Model):
    _inherit = 'ir.actions.act_window'

    # do not use new api, as read can return a single id or multi...
#     def read(self, fields=None, load='_classic_read'):

    def read(self, cr, uid, ids,
             fields=None, context=None, load='_classic_read'):
        """ call the method get_empty_list_help of the model and set the
        window action help message
        """
        ids_int = isinstance(ids, (int, long))
        if ids_int:
            ids = [ids]

        actions = super(IRActionsWindow, self).read(
            cr, uid, ids, fields=fields, context=context, load=load)
        for action in actions:
            if action.get('res_model', '') == 'res.partner':
                # By default, only show standalone contact
                action_context = action.get('context', '{}') or '{}'
                if 'search_show_all_positions' not in action_context:
                    action['context'] = action_context.replace(
                        '{',
                        ("{'search_show_all_positions': "
                         "{'is_set': True, 'set_value': False},"),
                        1)

        if ids_int:
            return actions[0]
        return actions
