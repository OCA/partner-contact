# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import _, api, models
from openerp.exceptions import ValidationError

from openerp.addons.partner_multi_relation.models.res_partner_relation_all \
    import register_select_specification


# Register relation from address partner to parent partner:
register_select_specification(
    base_name='partner_address',
    is_inverse=False,
    select_sql="""\
SELECT
    (partner.id * %%(padding)s) + %(key_offset)s as ID,
    'res.partner' AS res_model,
    partner.id AS res_id,
    partner.id AS left_partner_id,
    partner.parent_id AS right_partner_id,
    rprt.id AS type_id,
    NULL AS date_start,
    NULL AS date_end,
    %(is_inverse)s AS is_inverse
 FROM res_partner partner
 JOIN res_partner_relation_type rprt ON partner.type = rprt.partner_type
 WHERE NOT partner.parent_id IS NULL
   AND rprt.partner_synchronization_active""")

# Register relation from parent partner to address partner:
register_select_specification(
    base_name='partner_address',
    is_inverse=True,
    select_sql="""\
SELECT
    (partner.id * %%(padding)s) + %(key_offset)s as ID,
    'res.partner' AS res_model,
    partner.id AS res_id,
    partner.parent_id AS left_partner_id,
    partner.id AS right_partner_id,
    rprt.id AS type_id,
    NULL AS date_start,
    NULL AS date_end,
    %(is_inverse)s AS is_inverse
 FROM res_partner partner
 JOIN res_partner_relation_type rprt ON partner.type = rprt.partner_type
 WHERE NOT partner.parent_id IS NULL
   AND rprt.partner_synchronization_active""")


class ResPartnerRelationAll(models.AbstractModel):
    """Show addresses as relations if so configured."""
    _inherit = 'res.partner.relation.all'

    def _get_active_selects(self):
        """Return selects actually to be used.

        Selects are registered from all modules PRESENT. But should only be
        used to build view if module actually INSTALLED.
        """
        return super(ResPartnerRelationAll, self)._get_active_selects() +\
            ['partner_address', 'partner_address_inverse']

    @api.model
    def _compute_base_name(self, type_selection):
        """This will be overridden for each inherit model."""
        if type_selection.type_id.partner_type:
            return 'partner_address'
        return super(ResPartnerRelationAll, self)._compute_base_name(
            type_selection)

    @api.model
    def create_resource(self, vals, type_selection):
        if self._compute_base_name(type_selection) != 'partner_address':
            return super(ResPartnerRelationAll, self).create_resource(
                vals, type_selection)
        partner_model = self.env['res.partner']
        relation_type = type_selection.type_id
        if not relation_type.partner_synchronization_active:
            raise ValidationError(
                _("Creating a relation for address with type %s is"
                    " not allowed at this time.") %
                (relation_type.partner_type, ))
        left_partner = partner_model.browse(vals['left_partner_id'])
        left_partner.write({
            'type': relation_type.partner_type,
            'parent_id': vals['right_partner_id']})
        return left_partner

    @api.multi
    def write_resource(self, base_resource, vals):
        """Synchronize parent_id in left partner with connection.

        - If changed to non contact type, clear parent_id in partner;
        - If changed to contact type, set parent_id and contact type
          in partner.
        """
        self.ensure_one()
        # Determine old and new type
        type_model = self.env['res.partner.relation.type']
        vals_type = 'type_id' in vals and \
            type_model.browse(vals['type_id']) or False
        type_selection = self.type_selection_id
        old_type = type_selection.type_id
        new_type = vals_type or old_type
        # If neither old, nor new type are for partner address,
        # write can/should be handled by super method:
        if not old_type.partner_type and not new_type.partner_type:
            return super(ResPartnerRelationAll, self).write_resource(
                base_resource, vals)
        # We have to handle partner address:
        partner_model = self.env['res.partner']
        vals_left_partner = 'left_partner_id' in vals and \
            partner_model.browse(vals['left_partner_id']) or False
        vals_right_partner = 'right_partner_id' in vals and \
            partner_model.browse(vals['right_partner_id']) or False
        # Store existing values
        existing_left_partner = base_resource
        existing_right_partner = base_resource.parent_id
        left_partner = vals_left_partner or existing_left_partner
        right_partner = vals_right_partner or existing_right_partner
        # Relatively simple case is where non address
        #  connection is replaced by address connection
        if not old_type.partner_type:
            # Unlink existing connection
            super(ResPartnerRelationAll, self).unlink()
            # Create new connection
            left_partner.write({
                'type': new_type.partner_type,
                'parent_id': right_partner.id})
            return True
        # Handle case where address connection is changed into
        # regular connection:
        if not new_type.partner_type:
            # Clear existing parent:
            existing_left_partner.write({'parent_id': False})
            # Now create new connection:
            relation_model = self.env['res.partner.relation']
            vals['left_partner_id'] = left_partner.id
            vals['type_id'] = new_type.id
            vals['right_partner_id'] = right_partner.id
            relation_model.create(vals)
            return True
        # If we get here, both old and new connection are for address:
        # Check wether new type is already allowed:
        if not new_type.partner_synchronization_active:
            raise ValidationError(
                _("Creating a relation for address with type %s is"
                    " not allowed at self time.") %
                (new_type.partner_type, ))
        # If left partner changed, clear parent on left partner:
        existing_left_partner.write({'parent_id': False})
        left_partner.write({
            'type': new_type.partner_type,
            'parent_id': right_partner.id})
        return True

    @api.multi
    def unlink_resource(self, base_resource):
        """Deleting an address connection is clearing parent_id."""
        self.ensure_one()
        type_selection = self.type_selection_id
        if self._compute_base_name(type_selection) != 'partner_address':
            return super(ResPartnerRelationAll, self).unlink_resource(
                base_resource)
        base_resource.write({'parent_id': False})
