# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import _, api, models
from odoo.exceptions import UserError


class ResPartnerRelation(models.Model):
    _inherit = 'res.partner.relation'

    def relation_exists(self, left, type_rel):
        relation = self.search([
            ('left_partner_id', '=', left),
            ('type_id', '=', type_rel),
        ])
        return relation

    @api.multi
    def write(self, vals):
        part_mod = self.env['res.partner']
        type_relation = self.env.ref(
            'partner_multi_relation_parent.parent_relation_type'
        ).id
        for this in self:
            if this.type_id != type_relation:
                continue
            # check that whatever relation will come out of this write does
            # not exist already , but check only if type_id doesn't change, if
            # it does we don't care about uniqueness
            if vals.get('type_id', this.type_id) == type_relation:
                relation = this.relation_exists(
                    vals.get('left_partner_id', this.left_partner_id),
                    type_relation,
                    vals.get('right_partner_id', this.right_partner_id)
                )
                if relation:
                    raise UserError(_(
                        "The relation you are creating exists and has id %s"
                        "there can only be one relation of type %s" % (
                            str(relation.id), relation.type_id.name
                        )))
            if 'type_id' in vals and vals['type_id'] != type_relation:
                this.left_partner_id.with_context(
                    no_relation_update=True
                ).write({'parent_id': False})
            elif 'right_partner_id' in vals and 'left_partner_id' not in vals:
                new_parent = vals.get('right_partner_id')
                contact_id = this.left_partner_id
                contact_id.with_context(no_relation_update=True).write(
                    {'parent_id': new_parent}
                )
            elif 'left_partner_id' in vals and 'right_partner_id' not in vals:
                old_contact_id = part_mod.browse(this.left_partner_id)
                old_contact_id.with_context(no_relation_update=True).write(
                    {'parent_id': False}
                )
                contact_id = part_mod.browse(vals['left_partner_id'])
                contact_id.with_context(no_relation_update=True).write(
                    {'parent_id': this.right_partner_id}
                )
            elif 'left_partner_id' in vals and 'right_partner_id' in vals:
                old_contact_id = this.left_partner_id
                old_contact_id.with_context(no_relation_update=True).write(
                    {'parent_id': False}
                )
                contact_id = part_mod.browse(vals['left_partner_id'])
                contact_id.with_context(no_relation_update=True).write(
                    {'parent_id': vals['right_partner_id']},
                )
        res = super(ResPartnerRelation, self).write(vals=vals)
        return res

    @api.multi
    def unlink(self):
        type_relation = self.env.ref(
            'partner_multi_relation_parent.parent_relation_type'
        ).id
        for this in self:
            if this.type_id.id != type_relation:
                continue
            this.left_partner_id.with_context(no_relation_update=True).write(
                {'parent_id': False}
            )
        res = super(ResPartnerRelation, self).unlink()
        return res

    @api.model
    def create(self, vals):
        type_relation = self.env.ref(
            'partner_multi_relation_parent.parent_relation_type'
        ).id
        current = self.relation_exists(
            vals['left_partner_id'],
            type_relation,
        )
        if current:
            # we are creating a relation but one already exists, raise an
            # exception to warn the user relations of type_relation must be
            # unique.
            raise UserError(_(
                "The relation you are creating exists and has id %s"
                "there can only be one relation of type %s" % (
                    str(current.id), current.type_id.name
                )))
        # there is no relation, so we can create it, but we must update
        # the parent_id of the left contact of this new relation
        res = super(ResPartnerRelation, self).create(vals=vals)
        res.left_partner_id.with_context(no_relation_update=True).write(
            {'parent_id': vals['right_partner_id']}
        )
        return res
