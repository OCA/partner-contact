# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm
from openerp import SUPERUSER_ID

from ..tablib import Tab


class ResPartnerRelationType(orm.Model):
    _inherit = 'res.partner.relation.type'

    _columns = {
        'own_tab_left': fields.boolean('Show in own tab'),
        'own_tab_right': fields.boolean('Show in own tab'),
    }

    _defaults = {
        'own_tab_left': False,
        'own_tab_right': False,
    }

    def get_tabs(self, cr):
        tabs = []
        tab_domain = [
            '|',
            ('own_tab_left', '=', True),
            ('own_tab_right', '=', True)]
        tab_type_ids = self.search(cr, SUPERUSER_ID, tab_domain)
        for this in self.browse(cr, SUPERUSER_ID, tab_type_ids):
            if this.own_tab_left:
                new_tab = Tab(this, 'left')
                tabs.append(new_tab)
            if this.own_tab_right:
                new_tab = Tab(this, 'right')
                tabs.append(new_tab)
        return tabs

    def create(self, cr, uid, vals, context=None):
        new_type_id = super(ResPartnerRelationType, self).create(
            cr, uid, vals, context=context)
        this = self.browse(cr, uid, new_type_id, context=context)
        partner_model = self.pool['res.partner']
        if this.own_tab_left:
            new_tab = Tab(this, 'left')
            partner_model._add_tab_field(new_tab)
        if this.own_tab_right:
            new_tab = Tab(this, 'right')
            partner_model._add_tab_field(new_tab)
        return new_type_id

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
