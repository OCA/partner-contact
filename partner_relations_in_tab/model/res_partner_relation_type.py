# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm

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

    def make_tab(self, source, side):
        new_tab = Tab(source, side)
        return new_tab

    def get_tabs(self, cr, uid, context=None):
        tabs = []
        tab_domain = self._get_tab_domain()
        tab_type_ids = self.search(cr, uid, tab_domain, context=context)
        for this in self.browse(cr, uid, tab_type_ids, context=context):
            if this.own_tab_left:
                tabs.append(self.make_tab(this, 'left'))
            if this.own_tab_right:
                tabs.append(self.make_tab(this, 'right'))
        return tabs

    def _get_tab_domain(self):
        return [
            '|', ('own_tab_left', '=', True), ('own_tab_right', '=', True)]
