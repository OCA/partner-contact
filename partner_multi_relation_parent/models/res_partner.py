# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def update_relations(self, update=False):
        """Update contact relations.

        - Create for contact addresses.
        - Delete for other addresses.
        """
        if self.env.context.get('no_relation_update'):
            return
        relation_model = self.env['res.partner.relation']
        type_relation = self.env.ref(
            'partner_multi_relation_parent.parent_relation_type'
        )
        for this in self:
            if not update:
                existing_relation = None
            else:
                existing_relation = relation_model.search([
                    ('left_partner_id', '=', this.id),
                    ('type_id', '=', type_relation.id),
                ])
            # If not or no longer a contact, then delete relations:
            if this.type != 'contact' or not this.parent_id:
                if existing_relation:
                    existing_relation.unlink()
            else:
                # We have a contact, create or update relation if needed:
                if not existing_relation:
                    relation_model.create({
                        'left_partner_id': this.id,
                        'type_id': type_relation.id,
                        'right_partner_id': this.parent_id.id,
                    })
                else:
                    if existing_relation.right_partner_id != this.parent_id:
                        existing_relation.write({
                            'right_partner_id': this.parent_id.id,
                        })

    @api.model
    def create(self, vals):
        if self.env.context.get('partner_synchronization_active'):
            return super(ResPartner, self).create(vals)
        new_partner = self.with_context(
            partner_coordinated=True,
        ).create(vals)
        if new_partner.parent_id and new_partner.type:
            relation_type = type_model.search([
                ('partner_type', '=', new_partner.type),
                ('partner_synchronization_active', '=', True),
            ])
            if relation_type:
                self.with_context(
                    partner_synchronization_active=True,
                ).create({
                    'left_partner_id': new_partner.id,
                    'type_id': relation_type.id,
                    'right_partner_id': new_partner.parent_id.id,
                })
        return new_partner

    @api.multi
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        self.update_relations(update=True)
        return res
