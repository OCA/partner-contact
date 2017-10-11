# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import _, api, models
from odoo.exceptions import ValidationError


class ResPartnerRelation(models.Model):
    _inherit = 'res.partner.relation'

    @api.one
    @api.constrains(
        'left_partner_id',
        'type_id',
    )
    def _check_parent_relation(self):
        """A partner can only have one parent connection."""
        # TODO: Check for other parent type connections and partner type:
        if not self.left_partner_id.parent_id or \
                not self.type_id.partner_synchronization_active:
            return True
        existing = self.search([
            ('left_partner_id', '=', self.left_partner_id.id),
            ('type_id', '=', self.type_id.id),
            ('id', '!=', self.id),
        ])
        if existing:
            # we are creating a relation but one already exists, raise an
            # exception to warn the user relations of type_relation must
            # be unique.
            raise ValidationError(_(
                "The relation you are creating exists and has id %d.\n"
                "There can only be one relation of type %s" %
                (existing.id, self.type_id.name)
            ))

    @api.multi
    def update_left_partner(self):
        type_relation = self.get_contact_relation_type()
        for this in self:
            if this.type_id == type_relation:
                this.left_partner_id.with_context(
                    no_relation_update=True
                ).write({
                    'parent_id': this.right_partner_id.id,
                    'type': 'contact',
                })

    @api.multi
    def write(self, vals):
        """Synchronize parent_id in left partner with connection.

        - If changed to non contact type, clear parent_id in partner;
        - If changed to contact type, set parent_id and contact type
          in partner.
        """
        for this in self:
            # Clear parent if needed:
            if (this.type_id == type_relation and
                    (('type_id' in vals and
                      vals['type_id'] != type_relation.id) or
                     ('left_partner_id' in vals and
                      vals['left_partner_id'] != this.left_partner_id.id))):
                this.left_partner_id.with_context(
                    no_relation_update=True
                ).write({'parent_id': False})
        res = super(ResPartnerRelation, self).write(vals)
        self.update_left_partner()
        return res

    @api.multi
    def unlink(self):
        for this in self:
            if not this.type_id.partner_synchronization_active:
                continue
            this.left_partner_id.with_context(
                partner_synchronization_active=True
            ).write({'parent_id': False})
        return super(ResPartnerRelation, self).unlink()

    @api.model
    def create(self, vals):
        new_relation = super(ResPartnerRelation, self).create(vals)
        if self.env.context.get('partner_synchronization_active'):
            return new_relation
        # If enabled in relation type, update partner to have parent
        if new_relation.type_id.partner_synchronization_active:
            new_relation.left_partner_id.with_context(
                partner_synchronization_active=True,
            ).write({
                'type': new_relation.type_id.partner_type,
                'parent_id': new_relation.right_partner_id.id,
            })
        return new_relation
