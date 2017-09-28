# -*- coding: utf-8 -*-
# Copyright 2017-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResPartnerRelation(models.Model):
    _inherit = 'res.partner.relation'

    @api.model
    def create(self, vals):
        """Prevent contradictory links in hierarchy.

        We should not do this in a constraint, as those are only checked
        after creation has already been done, and other modules might
        fail when they process in invalid hierarchy when triggered on
        create.

        TODO: Prevent this also on write.
        """
        context = self.env.context
        if 'left_partner_id' not in vals and context.get('active_id'):
            vals['left_partner_id'] = context.get('active_id')
        # Check if we have needed left partner, type and right
        # partner. If not leave error handling to super
        if not {'left_partner_id', 'type_id', 'right_partner_id'} <= set(vals):
            return super(ResPartnerRelation, self).create(vals)
        type_model = self.env['res.partner.relation.type']
        type_id = type_model.browse(vals['type_id'])
        hierarchy = type_id.hierarchy
        # If relation is not for a hierarchy, just return super
        if hierarchy == 'equal':
            return super(ResPartnerRelation, self).create(vals)
        partner_model = self.env['res.partner']
        left_partner = partner_model.browse(vals['left_partner_id'])
        right_partner = partner_model.browse(vals['right_partner_id'])
        if ((hierarchy == 'left' and right_partner.is_above(left_partner)) or
                (hierarchy == 'right' and
                 left_partner.is_above(right_partner))):
            raise ValidationError(
                _("Not allowed to create an inconsistent hierarchy"))
        # Everything is OK, call super
        return super(ResPartnerRelation, self).create(vals)
