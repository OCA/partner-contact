# -*- coding: utf-8 -*-
# © 2013-2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import numbers
from openerp import _, models, fields, exceptions, api
from openerp.osv.expression import is_leaf, OR, FALSE_LEAF

PADDING = 10


class ResPartner(models.Model):
    _inherit = 'res.partner'

    relation_count = fields.Integer(
        'Relation Count',
        compute="_compute_relation_count"
    )

    relation_ids = fields.One2many(
        'res.partner.relation', string='Relations',
        compute='_compute_relation_ids',
        selectable=False,
    )

    relation_all_ids = fields.One2many(
        'res.partner.relation.all', 'this_partner_id',
        string='All relations with current partner',
        auto_join=True, selectable=False, copy=False,
    )

    search_relation_id = fields.Many2one(
        'res.partner.relation.type.selection', compute=lambda self: None,
        search='_search_relation_id', string='Has relation of type',
    )

    search_relation_partner_id = fields.Many2one(
        'res.partner', compute=lambda self: None,
        search='_search_related_partner_id', string='Has relation with',
    )

    search_relation_date = fields.Date(
        compute=lambda self: None, search='_search_relation_date',
        string='Relation valid',
    )

    search_relation_partner_category_id = fields.Many2one(
        'res.partner.category', compute=lambda self: None,
        search='_search_related_partner_category_id',
        string='Has relation with a partner in category',
    )

    @api.one
    @api.depends("relation_ids")
    def _compute_relation_count(self):
        """Count the number of relations this partner has for Smart Button

        Don't count inactive relations.
        """
        self.relation_count = len([r for r in self.relation_ids if r.active])

    @api.multi
    def _compute_relation_ids(self):
        '''getter for relation_ids'''
        self.env.cr.execute(
            "select p.id, array_agg(r.id) "
            "from res_partner p join res_partner_relation r "
            "on r.left_partner_id=p.id or r.right_partner_id=p.id "
            "where p.id in %s "
            "group by p.id",
            (tuple(self.ids),)
        )
        partner2relation = dict(self.env.cr.fetchall())
        for this in self:
            this.relation_ids += self.env['res.partner.relation'].browse(
                partner2relation.get(this.id, []),
            )

    @api.model
    def _search_relation_id(self, operator, value):
        result = []

        if operator not in [
            '=', '!=', 'like', 'not like', 'ilike', 'not ilike', 'in', 'not in'
        ]:
            raise exceptions.ValidationError(
                _('Unsupported search operator "%s"') % operator)

        relation_type_selection = []

        if operator == '=' and isinstance(value, numbers.Integral):
            relation_type_selection += self\
                .env['res.partner.relation.type.selection']\
                .browse(value)
        elif operator == '!=' and isinstance(value, numbers.Integral):
            relation_type_selection = self\
                .env['res.partner.relation.type.selection']\
                .search([
                    ('id', operator, value),
                ])
        else:
            relation_type_selection = self\
                .env['res.partner.relation.type.selection']\
                .search([
                    ('type_id.name', operator, value),
                ])

        if not relation_type_selection:
            result = [FALSE_LEAF]

        for relation_type in relation_type_selection:
            type_id, is_inverse = relation_type.get_type_from_selection_id()

            result = OR([
                result,
                [
                    '&',
                    ('relation_all_ids.type_id', '=', type_id),
                    (
                        'relation_all_ids.record_type', 'in',
                        ['a', 'b']
                        if relation_type.type_id.symmetric
                        else
                        (['b'] if is_inverse else ['a'])
                    )
                ],
            ])

        return result

    @api.model
    def _search_related_partner_id(self, operator, value):
        return [
            ('relation_all_ids.other_partner_id', operator, value),
        ]

    @api.model
    def _search_relation_date(self, operator, value):
        if operator != '=':
            raise exceptions.ValidationError(
                _('Unsupported search operator "%s"') % operator)

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
        return [
            ('relation_all_ids.other_partner_id.category_id', operator, value),
        ]

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # inject searching for current relation date if we search for relation
        # properties and no explicit date was given
        date_args = []
        for arg in args:
            if is_leaf(arg) and arg[0].startswith('search_relation'):
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
                if is_leaf(arg) and arg[0].startswith('search_relation'):
                    active_args = [('relation_all_ids.active', '=', True)]
                    break

        return super(ResPartner, self).search(
            args + date_args + active_args, offset=offset, limit=limit,
            order=order, count=count)

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        return super(ResPartner, self.with_partner_relations_context())\
            .read(fields=fields, load=load)

    @api.multi
    def write(self, vals):
        return super(ResPartner, self.with_partner_relations_context())\
            .write(vals)

    @api.multi
    def with_partner_relations_context(self):
        context = dict(self.env.context)
        if context.get('active_model', self._name) == self._name:
            existing = self.exists()
            context.setdefault(
                'active_id', existing.ids[0] if existing.ids else None)
            context.setdefault('active_ids', existing.ids)
            context.setdefault('active_model', self._name)
        return self.with_context(context)

    @api.multi
    def get_partner_type(self):
        """Get partner type for relation.
        :return: 'c' for company or 'p' for person
        :rtype: str
        """
        self.ensure_one()
        return 'c' if self.is_company else 'p'
