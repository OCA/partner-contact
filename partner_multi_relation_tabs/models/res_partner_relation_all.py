# -*- coding: utf-8 -*-
# Copyright 2014-2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class ResPartnerRelationAll(models.AbstractModel):
    """Abstract model to show each relation from two sides."""
    _inherit = 'res.partner.relation.all'

    tab_id = fields.Many2one(
        comodel_name='res.partner.tab',
        string='Show relation on tab',
        readonly=True,
    )

    def _get_additional_view_fields(self):
        """Add tab_id to view fields."""
        return ','.join([
            super(ResPartnerRelationAll, self)._get_additional_view_fields(),
            "CASE"
            "    WHEN NOT bas.is_inverse"
            "    THEN lefttab.id"
            "    ELSE righttab.id"
            " END as tab_id"])

    def _get_additional_tables(self):
        """Add res_partner_tab table to view."""
        return ' '.join([
            super(ResPartnerRelationAll, self)._get_additional_tables(),
            "LEFT OUTER JOIN res_partner_tab lefttab"
            " ON typ.tab_left_id = lefttab.id",
            "LEFT OUTER JOIN res_partner_tab righttab"
            " ON typ.tab_right_id = righttab.id"])

    @api.onchange(
        'this_partner_id',
        'other_partner_id',
    )
    def onchange_partner_id(self):
        """Add tab if needed to type_selection_id domain.

        This method makes sure then when a relation is added to a tab,
        it is with a relation type meant to be placed on that tab.
        """
        result = super(ResPartnerRelationAll, self).onchange_partner_id()
        if 'default_tab_id' in self.env.context:
            if 'domain' not in result:
                result['domain'] = {}
            if 'type_selection_id' not in result['domain']:
                result['domain']['type_selection_id'] = []
            selection_domain = result['domain']['type_selection_id']
            selection_domain.append(
                ('tab_id', '=', self.env.context['default_tab_id']))
        return result
