# -*- encoding: utf-8 -*-
##############################################################################
#
#    Partner Relation module for Odoo
#    Copyright (C) 2014-2015 Artisanat Monastique de Provence (www.barroux.org)
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
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
##############################################################################

from openerp.osv import orm, fields
from openerp.tools.translate import _


class res_partner_relation_type(orm.Model):
    _name = 'res.partner.relation.type'
    _description = "Partner Relation Type"
    _order = 'name'

    _columns = {
        'name': fields.char(
            'Relation Name', size=32, required=True, translate=True),
        'reverse_id': fields.many2one(
            'res.partner.relation.type', 'Reverse Relation Type',
            help="If the relation type is asymetric, select the corresponding "
            "reverse relation type. For exemple, 'A recommends B' is an "
            "asymetric relation ; it's reverse relation is 'B is recommended "
            "by A'. If the relation type is symetric, leave the field empty. "
            "For example, 'A is a competitor of B' is a symetric relation "
            "because we also have 'B is the competitor of A'."),
        'active': fields.boolean('Active'),
        }

    _defaults = {
        'active': True,
        }

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        current = self.browse(cr, uid, id, context=context)
        default.update({
            'name': u'%s (copy)' % current.name,
            'reverse_id': False,
            })
        return super(res_partner_relation_type, self).copy(
            cr, uid, id, default=default, context=context)

    def _get_reverse_relation_type_id(
            self, cr, uid, relation_type_id, context=None):
        relation_type = self.browse(
            cr, uid, relation_type_id, context=context)
        if relation_type.reverse_id:
            reverse_relation_type_id = relation_type.reverse_id.id
        else:
            reverse_relation_type_id = relation_type_id
        return reverse_relation_type_id

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        new_id = super(res_partner_relation_type, self).create(
            cr, uid, vals, context=context)
        if vals.get('reverse_id'):
            ctx_write = context.copy()
            ctx_write['allow_write_reverse_id'] = True
            self.write(
                cr, uid, vals['reverse_id'],
                {'reverse_id': new_id}, context=ctx_write)
        return new_id

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        if (
                'reverse_id' in vals
                and not context.get('allow_write_reverse_id')):
            raise orm.except_orm(
                _('Error:'),
                _('It is not possible to modify the reverse of a relation '
                    'type. You should desactivate or delete this relation '
                    'type and create a new one.'))
        return super(res_partner_relation_type, self).write(
            cr, uid, ids, vals, context=context)


class res_partner_relation(orm.Model):
    _name = 'res.partner.relation'
    _description = 'Partner Relation'

    _columns = {
        'src_partner_id': fields.many2one(
            'res.partner', 'Source Partner', required=True),
        'relation_type_id': fields.many2one(
            'res.partner.relation.type', 'Relation Type', required=True),
        'dest_partner_id': fields.many2one(
            'res.partner', 'Destination Partner', required=True),
        }

    _sql_constraints = [(
        'src_dest_partner_relation_uniq',
        'unique(src_partner_id, dest_partner_id, relation_type_id)',
        'This relation already exists!'
        )]

    def create(self, cr, uid, vals, context=None):
        '''When a user creates a relation, Odoo creates the reverse
        relation automatically'''
        reverse_rel_type_id = self.pool['res.partner.relation.type'].\
            _get_reverse_relation_type_id(
                cr, uid, vals['relation_type_id'], context=context)
        # Create reverse relation
        super(res_partner_relation, self).create(
            cr, uid, {
                'relation_type_id': reverse_rel_type_id,
                'src_partner_id': vals['dest_partner_id'],
                'dest_partner_id': vals['src_partner_id'],
                }, context=context)
        return super(res_partner_relation, self).create(
            cr, uid, vals, context=context)

    def _get_reverse_relation_id(self, cr, uid, relation, context=None):
        reverse_rel_type_id = self.pool['res.partner.relation.type'].\
            _get_reverse_relation_type_id(
                cr, uid, relation.relation_type_id.id, context=context)
        reverse_rel_ids = self.search(
            cr, uid, [
                ('src_partner_id', '=', relation.dest_partner_id.id),
                ('dest_partner_id', '=', relation.src_partner_id.id),
                ('relation_type_id', '=', reverse_rel_type_id)
                ], context=context)
        assert len(reverse_rel_ids) == 1, \
            'A relation always has one reverse relation'
        return reverse_rel_ids[0]

    def unlink(self, cr, uid, ids, context=None):
        '''When a user deletes a relation, Odoo deletes the reverse
        relation automatically'''
        for relation in self.browse(cr, uid, ids, context=None):
            reverse_rel_id = self._get_reverse_relation_id(
                cr, uid, relation, context=context)
            if reverse_rel_id not in ids:
                ids.append(reverse_rel_id)
        return super(res_partner_relation, self).unlink(
            cr, uid, ids, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        '''When a user writes on a relation, we also have to update
        the reverse relation'''
        reverse_relation_ids = []
        for relation in self.browse(cr, uid, ids, context=None):
            reverse_rel_id = self._get_reverse_relation_id(
                cr, uid, relation, context=context)
            if reverse_rel_id in ids:
                raise orm.except_orm(
                    _('Error:'),
                    _("You cannot write the same values on the relation "
                        "and it's reverse relation."))
            assert reverse_rel_id not in reverse_relation_ids, \
                "Impossible: it's relation has it's own reverse relation."
            reverse_relation_ids.append(reverse_rel_id)
        reverse_vals = {}
        if 'src_partner_id' in vals:
            reverse_vals['dest_partner_id'] = vals['src_partner_id']
        if 'dest_partner_id' in vals:
            reverse_vals['src_partner_id'] = vals['dest_partner_id']
        if 'relation_type_id' in vals:
            reverse_vals['relation_type_id'] = \
                self.pool['res.partner.relation.type'].\
                _get_reverse_relation_type_id(
                    cr, uid, vals['relation_type_id'], context=context)
        super(res_partner_relation, self).write(
            cr, uid, reverse_relation_ids, reverse_vals, context=context)
        return super(res_partner_relation, self).write(
            cr, uid, ids, vals, context=context)

    def go_to_dest_partner(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'Only 1 ID'
        relation = self.browse(cr, uid, ids[0], context=context)
        action = {
            'name': self.pool['res.partner']._description,
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_type': 'form',
            'view_mode': 'form,tree,kanban',
            'target': 'current',
            'res_id': relation.dest_partner_id.id,
            }
        return action


class res_partner(orm.Model):
    _inherit = 'res.partner'

    _columns = {
        'relation_ids': fields.one2many(
            'res.partner.relation', 'src_partner_id', 'Partner Relations'),
        }

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default['relation_ids'] = False
        return super(res_partner, self).copy(
            cr, uid, id, default=default, context=context)
