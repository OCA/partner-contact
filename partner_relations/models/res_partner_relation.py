# -*- coding: utf-8 -*-
# © 2013-2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api, exceptions, _
from openerp.osv.expression import FALSE_LEAF
from .res_partner import PADDING


class ResPartnerRelation(models.Model):
    '''Model res.partner.relation is used to describe all links or relations
    between partners in the database.

    In many parts of the code we have to know whether the active partner is
    the left partner, or the right partner. If the active partner is the
    right partner we have to show the inverse name.

    Because the active partner is crucial for the working of partner
    relationships, we make sure on the res.partner model that the partner id
    is set in the context where needed.
    '''
    _name = 'res.partner.relation'
    _description = 'Partner relation'
    _order = 'active desc, date_start desc, date_end desc'

    type_selection_id = fields.Many2one(
        'res.partner.relation.type.selection',
        compute='_compute_fields',
        fnct_inv=lambda *args: None,
        string='Type',
    )

    partner_id_display = fields.Many2one(
        'res.partner',
        compute='_compute_fields',
        fnct_inv=lambda *args: None,
        string='Partner',
    )

    allow_self = fields.Boolean(related='type_id.allow_self')

    left_contact_type = fields.Selection(
        lambda s: s.env['res.partner.relation.type']._get_partner_types(),
        'Left Partner Type',
        compute='_compute_any_partner_id',
        store=True,
    )

    right_contact_type = fields.Selection(
        lambda s: s.env['res.partner.relation.type']._get_partner_types(),
        'Right Partner Type',
        compute='_compute_any_partner_id',
        store=True,
    )

    any_partner_id = fields.Many2many(
        'res.partner',
        string='Partner',
        compute='_compute_any_partner_id',
        search='_search_any_partner_id'
    )

    left_partner_id = fields.Many2one(
        'res.partner',
        string='Source Partner',
        required=True,
        auto_join=True,
        ondelete='cascade',
    )

    right_partner_id = fields.Many2one(
        'res.partner',
        string='Destination Partner',
        required=True,
        auto_join=True,
        ondelete='cascade',
    )

    type_id = fields.Many2one(
        'res.partner.relation.type',
        string='Type',
        required=True,
        auto_join=True,
    )

    date_start = fields.Date('Starting date')
    date_end = fields.Date('Ending date')
    active = fields.Boolean('Active', default=True)

    @api.multi
    def _compute_fields(self):
        for this in self:
            on_right_partner = this._on_right_partner()
            this.type_selection_id = self\
                .env['res.partner.relation.type.selection']\
                .browse(this.type_id.id * PADDING +
                        (on_right_partner and 1 or 0))
            this.partner_id_display = (
                this.left_partner_id
                if on_right_partner
                else this.right_partner_id
            )

    @api.onchange('type_selection_id')
    def _onchange_type_selection_id(self):
        '''Set domain on partner_id_display, when selection a relation type'''
        result = {
            'domain': {'partner_id_display': [FALSE_LEAF]},
        }
        if not self.type_selection_id:
            return result
        type_id, is_reverse = self.type_selection_id\
            .get_type_from_selection_id()
        self.type_id = self.env['res.partner.relation.type'].browse(type_id)
        partner_domain = []
        check_contact_type = self.type_id.contact_type_right
        check_partner_category = self.type_id.partner_category_right
        if is_reverse:
            # partner_id_display is left partner
            check_contact_type = self.type_id.contact_type_left
            check_partner_category = self.type_id.partner_category_left
        if check_contact_type == 'c':
            partner_domain.append(('is_company', '=', True))
        if check_contact_type == 'p':
            partner_domain.append(('is_company', '=', False))
        if check_partner_category:
            partner_domain.append(
                ('category_id', 'child_of', check_partner_category.ids))
        result['domain']['partner_id_display'] = partner_domain
        return result

    @api.one
    @api.depends('left_partner_id', 'right_partner_id')
    def _compute_any_partner_id(self):
        self.left_contact_type = self.left_partner_id.get_partner_type()
        self.right_contact_type = self.right_partner_id.get_partner_type()
        self.any_partner_id = self.left_partner_id + self.right_partner_id

    @api.model
    def _search_any_partner_id(self, operator, value):
        return [
            '|',
            ('left_partner_id', operator, value),
            ('right_partner_id', operator, value),
        ]

    @api.multi
    def _on_right_partner(self):
        '''Determine wether functions are called in a situation where the
        active partner is the right partner. Default False!
        '''
        return set(self.mapped('right_partner_id').ids) &\
            set(self.env.context.get('active_ids', []))

    @api.model
    def _correct_vals(self, vals):
        """Fill type and left and right partner id, according to whether
        we have a normal relation type or an inverse relation type
        """
        vals = vals.copy()
        if 'type_selection_id' not in vals:
            return vals

        type_id, is_reverse = self\
            .env['res.partner.relation.type.selection']\
            .browse(vals['type_selection_id'])\
            .get_type_from_selection_id()

        vals['type_id'] = type_id

        if self._context.get('active_id'):
            if is_reverse:
                vals['right_partner_id'] = self._context['active_id']
            else:
                vals['left_partner_id'] = self._context['active_id']
        if vals.get('partner_id_display'):
            if is_reverse:
                vals['left_partner_id'] = vals['partner_id_display']
            else:
                vals['right_partner_id'] = vals['partner_id_display']
        if vals.get('other_partner_id'):
            if is_reverse:
                vals['left_partner_id'] = vals['other_partner_id']
            else:
                vals['right_partner_id'] = vals['other_partner_id']
            del vals['other_partner_id']
        if vals.get('this_partner_id'):
            if is_reverse:
                vals['right_partner_id'] = vals['this_partner_id']
            else:
                vals['left_partner_id'] = vals['this_partner_id']
            del vals['this_partner_id']
        if vals.get('contact_type'):
            del vals['contact_type']
        return vals

    @api.multi
    def write(self, vals):
        """Override write to correct values, before being stored."""
        vals = self._correct_vals(vals)
        return super(ResPartnerRelation, self).write(vals)

    @api.model
    def create(self, vals):
        """Override create to correct values, before being stored."""
        vals = self._correct_vals(vals)
        return super(ResPartnerRelation, self).create(vals)

    @api.one
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        """End date should not be before start date, if not filled

        :raises exceptions.Warning: When constraint is violated
        """
        if (self.date_start and self.date_end and
                self.date_start > self.date_end):
            raise exceptions.Warning(
                _('The starting date cannot be after the ending date.')
            )

    @api.one
    @api.constrains('left_partner_id', 'type_id')
    def _check_partner_type_left(self):
        """Check left partner for required company or person

        :raises exceptions.Warning: When constraint is violated
        """
        self._check_partner_type("left")

    @api.one
    @api.constrains('right_partner_id', 'type_id')
    def _check_partner_type_right(self):
        """Check right partner for required company or person

        :raises exceptions.Warning: When constraint is violated
        """
        self._check_partner_type("right")

    @api.one
    def _check_partner_type(self, side):
        """Check partner to left or right for required company or person

        :param str side: left or right
        :raises exceptions.Warning: When constraint is violated
        """
        assert side in ['left', 'right']
        ptype = getattr(self.type_id, "contact_type_%s" % side)
        company = getattr(self, '%s_partner_id' % side).is_company
        if (ptype == 'c' and not company) or (ptype == 'p' and company):
            raise exceptions.Warning(
                _('The %s partner is not applicable for this relation type.') %
                side
            )

    @api.one
    @api.constrains('left_partner_id', 'right_partner_id')
    def _check_not_with_self(self):
        """Not allowed to link partner to same partner

        :raises exceptions.Warning: When constraint is violated
        """
        if self.left_partner_id == self.right_partner_id:
            if not self.allow_self:
                raise exceptions.Warning(
                    _('Partners cannot have a relation with themselves.')
                )

    @api.one
    @api.constrains('left_partner_id', 'right_partner_id', 'active')
    def _check_relation_uniqueness(self):
        """Forbid multiple active relations of the same type between the same
        partners

        :raises exceptions.Warning: When constraint is violated
        """
        if not self.active:
            return
        domain = [
            ('type_id', '=', self.type_id.id),
            ('active', '=', True),
            ('id', '!=', self.id),
            ('left_partner_id', '=', self.left_partner_id.id),
            ('right_partner_id', '=', self.right_partner_id.id),
        ]
        if self.date_start:
            domain += ['|', ('date_end', '=', False),
                            ('date_end', '>=', self.date_start)]
        if self.date_end:
            domain += ['|', ('date_start', '=', False),
                            ('date_start', '<=', self.date_end)]
        if self.search(domain):
            raise exceptions.Warning(
                _('There is already a similar relation with overlapping dates')
            )

    @api.multi
    def get_action_related_partners(self):
        '''return a window action showing a list of partners taking part in the
        relations names by ids. Context key 'partner_relations_show_side'
        determines if we show 'left' side, 'right' side or 'all' (default)
        partners.
        If active_model is res.partner.relation.all, left=this and
        right=other'''
        field_names = {}

        if self.env.context.get('active_model', self._name) == self._name:
            field_names = {
                'left': ['left'],
                'right': ['right'],
                'all': ['left', 'right']
            }
        elif self.env.context.get('active_model') ==\
                'res.partner.relation.all':
            field_names = {
                'left': ['this'],
                'right': ['other'],
                'all': ['this', 'other']
            }
        else:
            assert False, 'Unknown active_model!'

        partners = self.env['res.partner'].browse([])
        field_names = field_names[
            self.env.context.get('partner_relations_show_side', 'all')
        ]
        field_names = ['%s_partner_id' % n for n in field_names]

        for relation in self.env[self.env.context.get('active_model')].browse(
                self.ids):
            for name in field_names:
                partners += relation[name]

        return {
            'name': _('Related partners'),
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'domain': [('id', 'in', partners.ids)],
            'views': [(False, 'tree'), (False, 'form')],
            'view_type': 'form'
        }
