# -*- coding: utf-8 -*-
# © 2014-2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Abstract model to show each relation from two sides."""
from psycopg2.extensions import AsIs

from openerp import _, api, fields, models
from openerp.tools import drop_view_if_exists


PADDING = 10
_RECORD_TYPES = [
    ('a', 'Left partner to right partner'),
    ('b', 'Right partner to left partner'),
]


class ResPartnerRelationAll(models.AbstractModel):
    """Abstract model to show each relation from two sides."""
    _auto = False
    _log_access = False
    _name = 'res.partner.relation.all'
    _description = 'All (non-inverse + inverse) relations between partners'
    _order = (
        'this_partner_id, type_selection_id,'
        'date_end desc, date_start desc'
    )

    _additional_view_fields = []
    """append to this list if you added fields to res_partner_relation that
    you need in this model and related fields are not adequate (ie for sorting)
    You must use the same name as in res_partner_relation.
    Don't overwrite this list in your declaration but append in _auto_init:

    def _auto_init(self, cr, context=None):
        self._additional_view_fields.append('my_field')
        return super(ResPartnerRelationAll, self)._auto_init(
            cr, context=context)

    my_field = fields...
    """

    this_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='One Partner',
        required=True,
    )
    other_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Other Partner',
        required=True,
    )
    type_selection_id = fields.Many2one(
        comodel_name='res.partner.relation.type.selection',
        string='Relation Type',
        required=True,
    )
    relation_id = fields.Many2one(
        comodel_name='res.partner.relation',
        string='Relation',
        readonly=True,
    )
    record_type = fields.Selection(
        selection=_RECORD_TYPES,
        string='Record Type',
        readonly=True,
    )
    date_start = fields.Date('Starting date')
    date_end = fields.Date('Ending date')
    active = fields.Boolean(
        string='Active',
        help="Records with date_end in the past are inactive",
    )
    any_partner_id = fields.Many2many(
        comodel_name='res.partner',
        string='Partner',
        compute=lambda self: None,
        search='_search_any_partner_id'
    )

    def _auto_init(self, cr, context=None):
        drop_view_if_exists(cr, self._table)
        additional_view_fields = ','.join(self._additional_view_fields)
        additional_view_fields = (',' + additional_view_fields)\
            if additional_view_fields else ''
        cr.execute(
            """\
CREATE OR REPLACE VIEW %(table)s AS
    SELECT
        rel.id * %(padding)s AS id,
        rel.id AS relation_id,
        cast('a' AS CHAR(1)) AS record_type,
        rel.left_partner_id AS this_partner_id,
        rel.right_partner_id AS other_partner_id,
        rel.date_start,
        rel.date_end,
        (rel.date_end IS NULL OR rel.date_end >= current_date) AS active,
        rel.type_id * %(padding)s AS type_selection_id
        %(additional_view_fields)s
    FROM res_partner_relation rel
    UNION SELECT
        rel.id * %(padding)s + 1,
        rel.id,
        CAST('b' AS CHAR(1)),
        rel.right_partner_id,
        rel.left_partner_id,
        rel.date_start,
        rel.date_end,
        rel.date_end IS NULL OR rel.date_end >= current_date,
        CASE
            WHEN typ.is_symmetric THEN rel.type_id * %(padding)s
            ELSE rel.type_id * %(padding)s + 1
        END
        %(additional_view_fields)s
    FROM res_partner_relation rel
    JOIN res_partner_relation_type typ ON (rel.type_id = typ.id)
            """,
            {
                'table': AsIs(self._table),
                'padding': PADDING,
                'additional_view_fields': AsIs(additional_view_fields),
            }
        )
        return super(ResPartnerRelationAll, self)._auto_init(
            cr, context=context
        )

    @api.model
    def _search_any_partner_id(self, operator, value):
        """Search relation with partner, no matter on which side."""
        # pylint: disable=no-self-use
        return [
            '|',
            ('this_partner_id', operator, value),
            ('other_partner_id', operator, value),
        ]

    @api.multi
    def name_get(self):
        return {
            this.id: '%s %s %s' % (
                this.this_partner_id.name,
                this.type_selection_id.display_name,
                this.other_partner_id.name,
            )
            for this in self
        }

    @api.onchange('type_selection_id')
    def onchange_type_selection_id(self):
        """Add domain on partners according to category and contact_type."""

        def check_partner_domain(partner, partner_domain, side):
            """Check wether partner_domain results in empty selection
            for partner, or wrong selection of partner already selected.
            """
            warning = {}
            if partner:
                test_domain = [('id', '=', partner.id)] + partner_domain
            else:
                test_domain = partner_domain
            partner_model = self.env['res.partner']
            partners_found = partner_model.search(test_domain, limit=1)
            if not partners_found:
                warning['title'] = _('Error!')
                if partner:
                    warning['message'] = (
                        _('%s partner incompatible with relation type.') %
                        side.title()
                    )
                else:
                    warning['message'] = (
                        _('No %s partner available for relation type.') %
                        side
                    )
            return warning

        this_partner_domain = []
        other_partner_domain = []
        if self.type_selection_id.contact_type_this:
            this_partner_domain.append((
                'is_company', '=',
                self.type_selection_id.contact_type_this == 'c'
            ))
        if self.type_selection_id.partner_category_this:
            this_partner_domain.append((
                'category_id', 'in',
                self.type_selection_id.partner_category_this.ids
            ))
        if self.type_selection_id.contact_type_other:
            other_partner_domain.append((
                'is_company', '=',
                self.type_selection_id.contact_type_other == 'c'
            ))
        if self.type_selection_id.partner_category_other:
            other_partner_domain.append((
                'category_id', 'in',
                self.type_selection_id.partner_category_other.ids
            ))
        result = {'domain': {
            'this_partner_id': this_partner_domain,
            'other_partner_id': other_partner_domain,
        }}
        # Check wether domain results in no choice or wrong choice of partners:
        warning = {}
        if this_partner_domain:
            warning = check_partner_domain(
                self.this_partner_id, this_partner_domain, _('this')
            )
        if not warning and other_partner_domain:
            warning = check_partner_domain(
                self.other_partner_id, other_partner_domain, _('other')
            )
        if warning:
            result['warning'] = warning
        return result

    @api.onchange(
        'this_partner_id',
        'other_partner_id',
    )
    def onchange_partner_id(self):
        """Set domain on type_selection_id based on partner(s) selected."""

        def check_type_selection_domain(type_selection_domain):
            """If type_selection_id already selected, check wether it
            is compatible with the computed type_selection_domain. An empty
            selection can practically only occur in a practically empty
            database, and will not lead to problems. Therefore not tested.
            """
            warning = {}
            if not (type_selection_domain and self.type_selection_id):
                return warning
            test_domain = (
                [('id', '=', self.type_selection_id.id)] +
                type_selection_domain
            )
            type_model = self.env['res.partner.relation.type.selection']
            types_found = type_model.search(test_domain, limit=1)
            if not types_found:
                warning['title'] = _('Error!')
                warning['message'] = _(
                    'Relation type incompatible with selected partner(s).'
                )
            return warning

        type_selection_domain = []
        if self.this_partner_id:
            type_selection_domain += [
                '|',
                ('contact_type_this', '=', False),
                ('contact_type_this', '=',
                 self.this_partner_id.get_partner_type()),
                '|',
                ('partner_category_this', '=', False),
                ('partner_category_this', 'in',
                 self.this_partner_id.category_id.ids),
            ]
        if self.other_partner_id:
            type_selection_domain += [
                '|',
                ('contact_type_other', '=', False),
                ('contact_type_other', '=',
                 self.other_partner_id.get_partner_type()),
                '|',
                ('partner_category_other', '=', False),
                ('partner_category_other', 'in',
                 self.other_partner_id.category_id.ids),
            ]
        result = {'domain': {
            'type_selection_id': type_selection_domain,
        }}
        # Check wether domain results in no choice or wrong choice for
        # type_selection_id:
        warning = check_type_selection_domain(type_selection_domain)
        if warning:
            result['warning'] = warning
        return result

    @api.model
    def _correct_vals(self, vals):
        """Fill left and right partner from this and other partner."""
        vals = vals.copy()
        if 'this_partner_id' in vals:
            vals['left_partner_id'] = vals['this_partner_id']
            del vals['this_partner_id']
        if 'other_partner_id' in vals:
            vals['right_partner_id'] = vals['other_partner_id']
            del vals['other_partner_id']
        if 'type_selection_id' not in vals:
            return vals
        selection = self.type_selection_id.browse(vals['type_selection_id'])
        type_id = selection.type_id.id
        is_inverse = selection.is_inverse
        vals['type_id'] = type_id
        del vals['type_selection_id']
        # Need to switch right and left partner if we are in reverse id:
        if 'left_partner_id' in vals or 'right_partner_id' in vals:
            if is_inverse:
                left_partner_id = False
                right_partner_id = False
                if 'left_partner_id' in vals:
                    right_partner_id = vals['left_partner_id']
                    del vals['left_partner_id']
                if 'right_partner_id' in vals:
                    left_partner_id = vals['right_partner_id']
                    del vals['right_partner_id']
                if left_partner_id:
                    vals['left_partner_id'] = left_partner_id
                if right_partner_id:
                    vals['right_partner_id'] = right_partner_id
        return vals

    @api.multi
    def write(self, vals):
        """divert non-problematic writes to underlying table"""
        vals = self._correct_vals(vals)
        for rec in self:
            rec.relation_id.write(vals)
        return True

    @api.model
    def create(self, vals):
        """Divert non-problematic creates to underlying table.

        Create a res.partner.relation but return the converted id.
        """
        is_inverse = False
        if 'type_selection_id' in vals:
            selection = self.type_selection_id.browse(
                vals['type_selection_id']
            )
            is_inverse = selection.is_inverse
        vals = self._correct_vals(vals)
        res = self.relation_id.create(vals)
        return_id = res.id * PADDING + (is_inverse and 1 or 0)
        return self.browse(return_id)

    @api.multi
    def unlink(self):
        """divert non-problematic creates to underlying table"""
        # pylint: disable=arguments-differ
        for rec in self:
            rec.relation_id.unlink()
        return True
