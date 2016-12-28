# -*- coding: utf-8 -*-
# © 2013-2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Define the type of relations that can exist between partners."""
from openerp import _, api, fields, models
from openerp.exceptions import ValidationError
from openerp.osv.expression import AND, OR


HANDLE_INVALID_ONCHANGE = [
    ('restrict',
     _('Do not allow change that will result in invalid relations')),
    ('ignore',
     _('Allow existing relations that do not fit changed conditions')),
    ('end',
     _('End relations per today, if they do not fit changed conditions')),
    ('delete',
     _('Delete relations that do not fit changed conditions')),
]


class ResPartnerRelationType(models.Model):
    """Model that defines relation types that might exist between partners"""
    _name = 'res.partner.relation.type'
    _description = 'Partner Relation Type'
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )
    name_inverse = fields.Char(
        string='Inverse name',
        required=True,
        translate=True,
    )
    contact_type_left = fields.Selection(
        selection='get_partner_types',
        string='Left partner type',
    )
    contact_type_right = fields.Selection(
        selection='get_partner_types',
        string='Right partner type',
    )
    partner_category_left = fields.Many2one(
        comodel_name='res.partner.category',
        string='Left partner category',
    )
    partner_category_right = fields.Many2one(
        comodel_name='res.partner.category',
        string='Right partner category',
    )
    allow_self = fields.Boolean(
        string='Reflexive',
        help='This relation can be set up with the same partner left and '
        'right',
        default=False,
    )
    is_symmetric = fields.Boolean(
        string='Symmetric',
        help="This relation is the same from right to left as from left to"
             " right",
        default=False,
    )
    handle_invalid_onchange = fields.Selection(
        selection=HANDLE_INVALID_ONCHANGE,
        string='Invalid relation handling',
        required=True,
        default='restrict',
        help="When adding relations criteria like partner type and category"
             " are checked.\n"
             "However when you change the criteria, there might be relations"
             " that do not fit the new criteria.\n"
             "Specify how this situation should be handled.",
    )

    @api.model
    def get_partner_types(self):
        """A partner can be an organisation or an individual."""
        # pylint: disable=no-self-use
        return [
            ('c', _('Organisation')),
            ('p', _('Person')),
        ]

    @api.onchange('is_symmetric')
    def onchange_is_symmetric(self):
        """Set right side to left side if symmetric."""
        if self.is_symmetric:
            self.update({
                'name_inverse': self.name,
                'contact_type_right': self.contact_type_left,
                'partner_category_right': self.partner_category_left,
            })

    @api.multi
    def check_existing(self, vals):
        """Check wether records exist that do not fit new criteria."""
        relation_model = self.env['res.partner.relation']

        def get_type_condition(vals, side):
            """Add if needed check for contact type."""
            fieldname1 = 'contact_type_%s' % side
            fieldname2 = '%s_partner_id.is_company' % side
            contact_type = fieldname1 in vals and vals[fieldname1] or False
            if contact_type == 'c':
                # Records that are not companies are invalid:
                return [(fieldname2, '=', False)]
            if contact_type == 'p':
                # Records that are companies are invalid:
                return [(fieldname2, '=', True)]
            return []

        def get_category_condition(vals, side):
            """Add if needed check for partner category."""
            fieldname1 = 'partner_category_%s' % side
            fieldname2 = '%s_partner_id.category_id' % side
            category_id = fieldname1 in vals and vals[fieldname1] or False
            if category_id:
                # Records that do not have the specified category are invalid:
                return [(fieldname2, 'not in', [category_id])]
            return []

        for rec in self:
            handling = (
                'handle_invalid_onchange' in vals and
                vals['handle_invalid_onchange'] or
                self.handle_invalid_onchange
            )
            if handling == 'ignore':
                continue
            invalid_conditions = []
            for side in ['left', 'right']:
                invalid_conditions = OR([
                    invalid_conditions,
                    get_type_condition(vals, side),
                ])
                invalid_conditions = OR([
                    invalid_conditions,
                    get_category_condition(vals, side),
                ])
            if not invalid_conditions:
                return
            # only look at relations for this type
            invalid_domain = AND([
                [('type_id', '=', rec.id)], invalid_conditions
            ])
            invalid_relations = relation_model.with_context(
                active_test=False
            ).search(invalid_domain)
            if invalid_relations:
                if handling == 'restrict':
                    raise ValidationError(
                        _('There are already relations not satisfying the'
                          ' conditions for partner type or category.')
                    )
                elif handling == 'delete':
                    invalid_relations.unlink()
                else:
                    # Delete future records, end other ones, ignore relations
                    # already ended:
                    cutoff_date = fields.Date.today()
                    for relation in invalid_relations:
                        if relation.date_start >= cutoff_date:
                            relation.unlink()
                        elif (not relation.date_end or
                                relation.date_end > cutoff_date):
                            relation.write({'date_end': cutoff_date})

    @api.multi
    def write(self, vals):
        """Handle existing relations if conditions change."""
        self.check_existing(vals)
        return super(ResPartnerRelationType, self).write(vals)
