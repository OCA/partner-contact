# -*- encoding: utf-8 -*-
##############################################################################
#
#    Partner Relation module for Odoo
#    Copyright (C) 2014-2015 Artisanat Monastique de Provence (www.barroux.org)
#    Copyright (C) 2015 Akretion France (www.akretion.com)
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

from openerp import models, fields, api, _
from openerp.exceptions import Warning


class ResPartnerRelationType(models.Model):
    _name = 'res.partner.relation.type'
    _description = "Partner Relation Type"
    _order = 'name'

    name = fields.Char(
        string='Relation Name', required=True, translate=True)
    reverse_id = fields.Many2one(
        'res.partner.relation.type', string='Reverse Relation Type',
        copy=False,
        help="If the relation type is asymetric, select the corresponding "
        "reverse relation type. For exemple, 'A recommends B' is an "
        "asymetric relation ; it's reverse relation is 'B is recommended "
        "by A'. If the relation type is symetric, leave the field empty. "
        "For example, 'A is a competitor of B' is a symetric relation "
        "because we also have 'B is the competitor of A'.")
    active = fields.Boolean(string='Active', default=True)

    @api.multi
    @api.returns('self')
    def _get_reverse_relation_type_id(self):
        self.ensure_one()
        if self.reverse_id:
            return self.reverse_id
        else:
            return self

    @api.model
    def create(self, vals):
        new = super(ResPartnerRelationType, self).create(vals)
        if vals.get('reverse_id'):
            reverse = self.browse(vals['reverse_id'])
            reverse.with_context(allow_write_reverse_id=True).write(
                {'reverse_id': new.id})
        return new

    @api.multi
    def write(self, vals):
        if (
                'reverse_id' in vals and
                not self.env.context.get('allow_write_reverse_id')):
            if vals['reverse_id'] != self.reverse_id.id:
                raise Warning(
                    _('It is not possible to modify the reverse of a relation '
                        'type. You should desactivate or delete this relation '
                        'type and create a new one.'))
        return super(ResPartnerRelationType, self).write(vals)


class ResPartnerRelation(models.Model):
    _name = 'res.partner.relation'
    _description = 'Partner Relation'

    src_partner_id = fields.Many2one(
        'res.partner', string='Source Partner', required=True)
    relation_type_id = fields.Many2one(
        'res.partner.relation.type', string='Relation Type', required=True)
    dest_partner_id = fields.Many2one(
        'res.partner', string='Destination Partner', required=True)

    _sql_constraints = [(
        'src_dest_partner_relation_uniq',
        'unique(src_partner_id, dest_partner_id, relation_type_id)',
        'This relation already exists!'
        )]

    @api.model
    def create(self, vals):
        '''When a user creates a relation, Odoo creates the reverse
        relation automatically'''
        assert vals.get('relation_type_id'), 'relation_type_id is required'
        rel_type = self.env['res.partner.relation.type'].browse(
            vals['relation_type_id'])
        reverse_rel_type = rel_type._get_reverse_relation_type_id()
        # Create reverse relation
        super(ResPartnerRelation, self).create({
            'relation_type_id': reverse_rel_type.id,
            'src_partner_id': vals['dest_partner_id'],
            'dest_partner_id': vals['src_partner_id'],
            })
        return super(ResPartnerRelation, self).create(vals)

    @api.multi
    @api.returns('self')
    def _get_reverse_relation(self):
        self.ensure_one()
        reverse_rel_type = self.relation_type_id.\
            _get_reverse_relation_type_id()
        reverse_rels = self.search([
            ('src_partner_id', '=', self.dest_partner_id.id),
            ('dest_partner_id', '=', self.src_partner_id.id),
            ('relation_type_id', '=', reverse_rel_type.id)
            ])
        assert len(reverse_rels) == 1, \
            'A relation always has one reverse relation'
        return reverse_rels[0]

    @api.multi
    def unlink(self):
        '''When a user deletes a relation, Odoo deletes the reverse
        relation automatically'''
        for relation in self:
            reverse_rel = relation._get_reverse_relation()
            if reverse_rel not in self:
                self += reverse_rel
        return super(ResPartnerRelation, self).unlink()

    @api.multi
    def write(self, vals):
        '''When a user writes on a relation, we also have to update
        the reverse relation'''
        reverse_relations = self.browse(False)
        for relation in self:
            reverse_rel = relation._get_reverse_relation()
            if reverse_rel in self:
                raise Warning(
                    _("You cannot write the same values on the relation "
                        "and it's reverse relation."))
            assert reverse_rel not in reverse_relations, \
                "Impossible: it's relation has it's own reverse relation."
            reverse_relations += reverse_rel
        reverse_vals = {}
        if 'src_partner_id' in vals:
            reverse_vals['dest_partner_id'] = vals['src_partner_id']
        if 'dest_partner_id' in vals:
            reverse_vals['src_partner_id'] = vals['dest_partner_id']
        if 'relation_type_id' in vals:
            rel_type = self.env['res.partner.relation.type'].browse(
                vals['relation_type_id'])
            reverse_vals['relation_type_id'] = \
                rel_type._get_reverse_relation_type_id().id
        super(ResPartnerRelation, reverse_relations).write(
            reverse_vals)
        return super(ResPartnerRelation, self).write(vals)

    @api.multi
    def go_to_dest_partner(self):
        self.ensure_one()
        action = {
            'name': self.env['res.partner']._description,
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_type': 'form',
            'view_mode': 'form,tree,kanban',
            'target': 'current',
            'res_id': self[0].dest_partner_id.id,
            }
        return action


class ResPartner(models.Model):
    _inherit = 'res.partner'

    relation_ids = fields.One2many(
        'res.partner.relation', 'src_partner_id', string='Partner Relations')
