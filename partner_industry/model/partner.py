# -*- coding: utf-8 -*-
# © 2015 Jacques-Etienne Baudoux <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, orm


class ResPartner(orm.Model):
    _inherit = 'res.partner'
    _columns = {
        'industry_id': fields.many2one(
            'res.partner.category.industry',
            'Industry Sector',
            ondelete='restrict'),
    }
