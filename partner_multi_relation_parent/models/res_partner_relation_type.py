# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Define synchronization between relations and addresses."""
from openerp import api, fields, models


class ResPartnerRelationType(models.Model):
    """Model that defines relation types that might exist between partners"""
    _inherit = 'res.partner.relation.type'

    partner_type = fields.Selection(
        # TODO: determine automatically from selection in res.partner
        selection=[
            ('contact', 'Contact'),
            ('invoice', 'Invoice address'),
            ('delivery', 'Shipping address'),
            ('other', 'Other address'),
        ],
        string='Partner Address Type',
        readonly=True,
        help="If filled connections will be automatically created when"
             " partners of the specified type are linked to a parent.\n"
             "Also the parent of the left contact will be updated when"
             " connections of this type are added or updated."
    )
    partner_synchronization_active = fields.Boolean(
        string="Synchronize relations and addresses",
        default=False,
        help="This field can only be true if Partner Address Type filled.\n"
             " When enabled will make sure that for all these connections"
             " the left partner will have the right partner as parent."
    )

    @api.multi
    def write(self, vals):
        """For address relation types, you can only change active flag."""
        for this in self:
            if not this.partner_type:
                super(ResPartnerRelationType, this).write(vals)
                continue
            if 'partner_synchronization_active' not in vals:
                continue  # Do nothing
            super(ResPartnerRelationType, this).write({
                'partner_synchronization_active':
                    vals['partner_synchronization_active']
            })
        return True
