# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# Copyright 2017 Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.addons.crm.wizard.base_partner_merge import MergePartnerAutomatic

    
class MergePartnerAutomaticPatch(models.TransientModel):
    _inherit = 'base.partner.merge.automatic.wizard'
    
    @api.multi
    def action_merge(self):
        res = super(MergePartnerAutomaticPatch, self.with_context(exclude_abstract_from_deduplicate=True)).action_merge()
        return res
    
class IRModelFields(models.Model):
    _inherit= 'ir.model.fields'
    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        res = super(IRModelFields, self).search(args, offset=offset, limit=limit, order=order, count=count)
        if self._context.get('exclude_abstract_from_deduplicate', False):
            res = res.filtered(lambda f: self.env[f.model]._abstract != True)
        return res
