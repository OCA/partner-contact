# -*- coding: utf-8 -*-
#
#
#    Authors: Guewen Baconnier
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    revision_ids = fields.One2many(comodel_name='res.partner.revision',
                                   inverse_name='partner_id',
                                   string='Revisions',
                                   readonly=True)
    count_pending_revisions = fields.Integer(
        string='Pending Revisions',
        compute='_count_pending_revisions',
        search='_search_count_pending_revisions')

    @api.one
    @api.depends('revision_ids', 'revision_ids.state')
    def _count_pending_revisions(self):
        revisions = self.revision_ids.filtered(
            lambda rev: rev.state == 'draft' and rev.partner_id == self
        )
        self.count_pending_revisions = len(revisions)

    @api.multi
    def write(self, values):
        if self.env.context.get('__no_revision'):
            return super(ResPartner, self).write(values)
        else:
            revision_model = self.env['res.partner.revision']
            for record in self:
                local_values = revision_model.add_revision(record, values)
                super(ResPartner, record).write(local_values)
        return True

    def _search_count_pending_revisions(self, operator, value):
        if operator not in ('=', '!=', '<', '<=', '>', '>=', 'in', 'not in'):
            return []
        query = ("SELECT p.id "
                 "FROM res_partner p "
                 "INNER JOIN res_partner_revision r ON r.partner_id = p.id "
                 "WHERE r.state = 'draft' "
                 "GROUP BY p.id "
                 "HAVING COUNT(r.id) %s %%s ") % operator
        self.env.cr.execute(query, (value,))
        ids = [row[0] for row in self.env.cr.fetchall()]
        return [('id', 'in', ids)]
