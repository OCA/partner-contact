# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import _, api, models
from odoo.exceptions import ValidationError


class ResPartnerRelation(models.Model):
    _inherit = 'res.partner.relation'

    @api.multi
    def write(self, vals):
        """Synchronize parent_id in left partner with connection.

        - If changed to non contact type, clear parent_id in partner;
        - If changed to contact type, set parent_id and contact type
          in partner.
        """
        type_model = self.env['res.partner.relation.type']
        partner_model = self.env['res.partner']
        vals_type = 'type_id' in vals and \
            type_model.browse(vals['type_id']) or False
        vals_left_partner = 'left_partner_id' in vals and \
            partner_model.browse(vals['left_partner_id']) or False
        vals_right_partner = 'right_partner_id' in vals and \
            partner_model.browse(vals['right_partner_id']) or False
        for this in self:
            # Determine old and new type
            old_type = this.type_id
            new_type = vals_type or old_type
            # First handle simple case: no address type involved
            if not old_type.partner_type and not new_type.partner_type:
                super(ResPartnerRelation, this).write(vals)
                continue
            # Store existing values
            existing_left_partner = this.left_partner_id
            existing_right_partner = this.right_partner_id
            left_partner = vals_left_partner or existing_left_partner
            right_partner = vals_right_partner or existing_right_partner
            # Second relatively simple case is where non address
            #  connection is replaced by address connection
            if not old_type.partner_type:
                # Unlink existing connection
                super(ResPartnerRelation, this).unlink()
                # Create new connection
                left_partner.write({
                    'type': new_type.partner_type,
                    'parent_id': right_partner.id,
                })
                continue
            # Third handle case where address connection is changed into
            # regular connection:
            if not new_type.partner_type:
                # Clear existing parent:
                existing_left_partner.write({
                    'parent_id': False,
                })
                # Now create new connection:
                vals['left_partner_id'] = left_partner.id
                vals['type_id'] = new_type.id
                vals['right_partner_id'] = right_partner.id
                super(ResPartnerRelation, this).create(vals)
                continue
            # If we get here, both old and new connection are for address:
            # Check wether new type is already allowed:
            if not new_type.partner_synchronization_active:
                raise ValidationError(
                    _("Creating a relation for address with type %s is"
                      " not allowed at this time.") %
                    (new_type.partner_type, ))
            # If left partner changed, clear parent on left partner:
            if left_partner != existing_left_partner:
                existing_left_partner.write({
                    'parent_id': False,
                })
            left_partner.write({
                'type': new_type.partner_type,
                'parent_id': right_partner.id,
            })
        return True

    @api.multi
    def unlink(self):
        """Unlinking relations for address, means clearing parent_id."""
        for this in self:
            if this.type_id.partner_type:
                this.left_partner_id.write({
                    'parent_id': False,
                })
                continue
            super(ResPartnerRelation, this).unlink()
        return True

    @api.model
    def create(self, vals):
        """Creating a relation for an address means updating parent."""
        type_model = self.env['res.partner.relation.type']
        partner_model = self.env['res.partner']
        relation_type = type_model.browse(vals['type_id'])
        if relation_type.partner_type:
            if not relation_type.partner_synchronization_active:
                raise ValidationError(
                    _("Creating a relation for address with type %s is"
                      " not allowed at this time.") %
                    (relation_type.partner_type, ))
            left_partner = partner_model.browse(vals['left_partner_id'])
            left_partner.write({
                'type': relation_type.partner_type,
                'parent_id': vals['right_partner_id'],
            })
            # Return the left partner.
            # Create in res_partner_relation_all will know what to do.
            return left_partner
        return super(ResPartnerRelation, self).create(vals)
