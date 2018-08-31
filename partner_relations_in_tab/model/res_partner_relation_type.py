# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.osv.orm import Model
from openerp.osv import fields


class ResPartnerRelationType(Model):
    _inherit = 'res.partner.relation.type'

    _columns = {
        'own_tab_left': fields.boolean('Show in own tab'),
        'own_tab_right': fields.boolean('Show in own tab'),
    }

    _defaults = {
        'own_tab_left': False,
        'own_tab_right': False,
    }

    def create(self, cr, uid, vals, context=None):
        relation_type_id = super(ResPartnerRelationType, self).create(
            cr, uid, vals, context=context)
        relation_type = self.browse(cr, uid, relation_type_id, context=context)
        partner_model = self.pool['res.partner']
        if relation_type.own_tab_left:
            tab = partner_model._make_tab(relation_type, 'left')
            partner_model._add_tab_field(tab)
        if relation_type.own_tab_right:
            tab = partner_model._make_tab(relation_type, 'right')
            partner_model._add_tab_field(tab)
        return relation_type_id

    def write(self, cr, uid, ids, vals, context=None):
        result = super(ResPartnerRelationType, self).write(
            cr, uid, ids, vals, context=context)
        partner_model = self.pool['res.partner']
        partner_model._update_tab_fields(cr)
        return result

    def unlink(self, cr, uid, ids, context=None):
        result = super(ResPartnerRelationType, self).unlink(
            cr, uid, ids, context=context)
        partner_model = self.pool['res.partner']
        partner_model._update_tab_fields(cr)
        return result
