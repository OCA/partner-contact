# -*- coding: utf-8 -*-
# © 2015 Jacques-Etienne Baudoux <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm


class Industry(orm.Model):
    _name = 'res.partner.category.industry'
    _description = 'Industry'
    _inherit = 'res.partner.category'
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

    _columns = {
        'code': fields.char('Code', size=16),
        'parent_id': fields.many2one(
            _name,
            'Parent %s' % _description, select=True, ondelete='cascade'),
        'partner_ids': fields.many2many(
            'res.partner',
            'res_partner_industry_rel', 'industry_id', 'partner_id',
            'Partners'),
    }
