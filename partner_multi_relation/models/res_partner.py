# Copyright 2013-2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Support connections between partners."""
import numbers

from odoo import _, api, exceptions, fields, models
from odoo.osv.expression import is_leaf, OR, FALSE_LEAF


class ResPartner(models.Model):
    """Extend partner with relations and allow to search for relations
    in various ways.
    """
    # pylint: disable=invalid-name
    # pylint: disable=no-member
    _inherit = 'res.partner'

    relation_count = fields.Integer(
        string='Relation Count',
        compute="_compute_relation_count"
    )
    relation_all_ids = fields.One2many(
        comodel_name='res.partner.relation.all',
        inverse_name='this_partner_id',
        string='All relations with current partner',
        auto_join=True,
        selectable=False,
        copy=False,
    )
    search_relation_type_id = fields.Many2one(
        comodel_name='res.partner.relation.type.selection',
        compute=lambda self: None,
        search='_search_relation_type_id',
        string='Has relation of type',
    )
    search_relation_partner_id = fields.Many2one(
        comodel_name='res.partner',
        compute=lambda self: None,
        search='_search_related_partner_id',
        string='Has relation with',
    )
    search_relation_date = fields.Date(
        compute=lambda self: None,
        search='_search_relation_date',
        string='Relation valid',
    )
    search_relation_partner_category_id = fields.Many2one(
        comodel_name='res.partner.category',
        compute=lambda self: None,
        search='_search_related_partner_category_id',
        string='Has relation with a partner in category',
    )

    @api.depends("relation_all_ids")
    def _compute_relation_count(self):
        """Count the number of relations this partner has for Smart Button

        Don't count inactive relations.
        """
        for rec in self:
            rec.relation_count = len(rec.relation_all_ids.filtered('active'))

    @api.model
    def _search_relation_type_id(self, operator, value):
        """Search partners based on their type of relations."""
        result = []
        SUPPORTED_OPERATORS = (
            '=',
            '!=',
            'like',
            'not like',
            'ilike',
            'not ilike',
            'in',
            'not in',
        )
        if operator not in SUPPORTED_OPERATORS:
            raise exceptions.ValidationError(
                _('Unsupported search operator "%s"') % operator)
        type_selection_model = self.env['res.partner.relation.type.selection']
        relation_type_selection = []
        if operator == '=' and isinstance(value, numbers.Integral):
            relation_type_selection += type_selection_model.browse(value)
        elif operator == '!=' and isinstance(value, numbers.Integral):
            relation_type_selection = type_selection_model.search([
                ('id', operator, value),
            ])
        else:
            relation_type_selection = type_selection_model.search([
                '|',
                ('type_id.name', operator, value),
                ('type_id.name_inverse', operator, value),
            ])
        if not relation_type_selection:
            result = [FALSE_LEAF]
        for relation_type in relation_type_selection:
            result = OR([
                result,
                [
                    ('relation_all_ids.type_selection_id.id', '=',
                     relation_type.id),
                ],
            ])
        return result

    @api.model
    def _search_related_partner_id(self, operator, value):
        """Find partner based on relation with other partner."""
        # pylint: disable=no-self-use
        return [
            ('relation_all_ids.other_partner_id', operator, value),
        ]

    @api.model
    def _search_relation_date(self, operator, value):
        """Look only for relations valid at date of search."""
        # pylint: disable=no-self-use
        return [
            '&',
            '|',
            ('relation_all_ids.date_start', '=', False),
            ('relation_all_ids.date_start', '<=', value),
            '|',
            ('relation_all_ids.date_end', '=', False),
            ('relation_all_ids.date_end', '>=', value),
        ]

    @api.model
    def _search_related_partner_category_id(self, operator, value):
        """Search for partner related to a partner with search category."""
        # pylint: disable=no-self-use
        return [
            ('relation_all_ids.other_partner_id.category_id', operator, value),
        ]

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """Inject searching for current relation date if we search for
        relation properties and no explicit date was given.
        """
        # pylint: disable=arguments-differ
        # pylint: disable=no-value-for-parameter
        date_args = []
        for arg in args:
            if (is_leaf(arg) and isinstance(arg[0], str) and
                    arg[0].startswith('search_relation')):
                if arg[0] == 'search_relation_date':
                    date_args = []
                    break
                if not date_args:
                    date_args = [
                        ('search_relation_date', '=', fields.Date.today()),
                    ]
        # because of auto_join, we have to do the active test by hand
        active_args = []
        if self.env.context.get('active_test', True):
            for arg in args:
                if (is_leaf(arg) and isinstance(arg[0], str) and
                        arg[0].startswith('search_relation')):
                    active_args = [('relation_all_ids.active', '=', True)]
                    break
        return super(ResPartner, self).search(
            args + date_args + active_args, offset=offset, limit=limit,
            order=order, count=count)

    @api.multi
    def get_partner_type(self):
        """Get partner type for relation.
        :return: 'c' for company or 'p' for person
        :rtype: str
        """
        self.ensure_one()
        return 'c' if self.is_company else 'p'

    @api.multi
    def action_view_relations(self):
        for contact in self:
            relation_model = self.env['res.partner.relation.all']
            relation_ids = relation_model.\
                search(['|',
                       ('this_partner_id', '=', contact.id),
                       ('other_partner_id', '=', contact.id)])
            action = self.env.ref(
                'partner_multi_relation.action_res_partner_relation_all'
            ).read()[0]
            action['domain'] = [('id', 'in', relation_ids.ids)]
            context = action.get('context', '{}').strip()[1:-1]
            elements = context.split(',') if context else []
            to_add = ["""'search_default_this_partner_id': {0},
                        'default_this_partner_id': {0},
                        'active_model': 'res.partner',
                        'active_id': {0},
                        'active_ids': [{0}],
                        'active_test': False""".format(contact.id)]
            context = '{' + ', '.join(elements + to_add) + '}'
            action['context'] = context
            return action
