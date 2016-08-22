# -*- coding: utf-8 -*-
# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def write(self, vals):
        if 'lang' in vals and vals['lang']:
            if 'child_ids' in vals:
                childs = self.browse(vals['child_ids'])
            else:
                childs = self.mapped('child_ids')
            childs = childs.filtered(lambda x: not x.lang)
            if childs:
                childs.write({'lang': vals['lang']})
        return super(ResPartner, self).write(vals)

    @api.multi
    def onchange_address(self, use_parent_address, parent_id):
        """Change language if the parent company changes and there's no
        language defined yet"""
        res = super(ResPartner, self).onchange_address(
            use_parent_address, parent_id)
        if parent_id and self.parent_id.id != parent_id and not self.lang:
            parent = self.browse(parent_id)
            val = res.setdefault('value', {})
            val['lang'] = parent.lang
        return res

    @api.multi
    @api.onchange('lang')
    def onchange_lang(self):
        if self.lang:
            childs = self.child_ids.filtered(lambda x: not x.lang)
            for child in childs:
                child.lang = self.lang
