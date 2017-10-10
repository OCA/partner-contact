# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import _, api, models
from odoo.exceptions import ValidationError


class ResPartnerRelation(models.Model):
    _inherit = 'res.partner.relation'

    def get_contact_relation_type(self):
        return self.env.ref(
            'partner_multi_relation_parent.parent_relation_type'
        )

    @api.one
    @api.constrains(
        'left_partner_id',
        'type_id',
    )
    def _only_one_contact(self):
        """A person can only be a contact for one partner."""
        type_relation = self.get_contact_relation_type()
        existing = self.search([
            ('left_partner_id', '=', self.left_partner_id.id),
            ('type_id', '=', type_relation.id),
            ('id', '!=', self.id),
        ])
        if existing:
            # we are creating a relation but one already exists, raise an
            # exception to warn the user relations of type_relation must
            # be unique.
            raise ValidationError(_(
                "The relation you are creating exists and has id %d.\n"
                "There can only be one relation of type %s" %
                (existing.id, type_relation.name)
            ))

    @api.multi
    def update_left_partner(self):
        type_relation = self.get_contact_relation_type()
        for this in self:
            if this.type_id == type_relation:
                this.left_partner_id.with_context(
                    no_relation_update=True
                ).write({
                    'parent_id': this.right_partner_id,
                    'type': 'contact',
                })

    @api.multi
    def write(self, vals):
        """Synchronize parent_id in left partner with connection.

        - If changed to non contact type, clear parent_id in partner;
        - If changed to contact type, set parent_id and contact type
          in partner.
        """
        type_relation = self.get_contact_relation_type()
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
        type_relation = self.get_contact_relation_type()
        for this in self:
            if this.type_id != type_relation:
                continue
            this.left_partner_id.with_context(
                no_relation_update=True
            ).write({'parent_id': False})
        return super(ResPartnerRelation, self).unlink()

    @api.model
    def create(self, vals):
        res = super(ResPartnerRelation, self).create(vals)
        res.update_left_partner()
        return res
