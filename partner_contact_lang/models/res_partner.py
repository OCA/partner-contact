# -*- coding: utf-8 -*-
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def write(self, vals):
        """Propagate a language change in the partner to the child contacts."""
        res = super(ResPartner, self).write(vals)
        if vals.get('lang'):
            childs = self.search([
                ('id', 'child_of', self.ids),
                ('lang', '=', False),
            ])
            if childs:
                childs.write({'lang': vals['lang']})
        return res

    @api.onchange('parent_id')
    def onchange_parent_id(self):
        """Change language if the parent company changes and there's no
        language defined yet"""
        res = super(ResPartner, self).onchange_parent_id()
        if self.parent_id and self.parent_id != self and not self.lang:
            val = res.setdefault('value', {})
            val['lang'] = self.parent_id.lang
        return res
