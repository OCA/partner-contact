# Copyright 2017-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from ..tablib import Tab


class ResPartnerTab(models.Model):
    """Model that defines relation types that might exist between partners"""
    _name = 'res.partner.tab'
    _description = 'Tabs to add to partner'
    _order = 'name'

    @api.model
    def get_partner_types(self):
        """Partner types are defined by model res.partner.relation.type."""
        # pylint: disable=no-self-use
        rprt_model = self.env['res.partner.relation.type']
        return rprt_model.get_partner_types()

    code = fields.Char(
        string='Code',
        required=True,
        help="Language independent code for tab")
    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
        help="Will provide title for tab in user language")
    contact_type = fields.Selection(
        selection='get_partner_types',
        string='Valid for partner type')
    partner_category_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Valid for partner category')
    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string="Partners with this tab",
        help="This tab will only show for certain partners.\n"
             "Do not combine this with selection for contact type or"
             " category.")

    @api.constrains('contact_type', 'partner_category_id', 'partner_ids')
    def _check_partner_ids(self):
        """If partner_ids filled, other domain fields should be empty."""
        if self.partner_ids and \
                (self.contact_type or self.partner_category_id):
            raise ValidationError(_(
                "You can not both specify partner_ids and other criteria."))

    @api.multi
    def update_types(self, vals=None):
        """Update types on write or unlink.

        If we have no vals, assume unlink.
        """
        if vals:
            contact_type = vals.get('contact_type', False)
            partner_category_id = vals.get('partner_category_id', False)
        type_model = self.env['res.partner.relation.type']
        for this in self:
            for tab_side in ('left', 'right'):
                side_tab = 'tab_%s_id' % tab_side
                tab_using = type_model.search([(side_tab, '=', this.id)])
                for relation_type in tab_using:
                    type_value = relation_type['contact_type_%s' % tab_side]
                    category_value = \
                        relation_type['partner_category_%s' % tab_side]
                    if (not vals or
                            (contact_type and contact_type != type_value) or
                            (partner_category_id and
                             partner_category_id != category_value.id)):
                        relation_type.write({side_tab: False})

    @api.multi
    def write(self, vals):
        """Remove tab from types no longer satifying criteria."""
        if vals.get('contact_type', False) or \
                vals.get('partner_category_id', False):
            self.update_types(vals)
        result = super(ResPartnerTab, self).write(vals)
        return result

    @api.multi
    def unlink(self):
        """Unlink should first remove references."""
        self.update_types()
        return super(ResPartnerTab, self).unlink()

    @api.model
    def get_tabs(self):
        """Convert information on tabs in database to array of objects."""
        tabs = [Tab(tab_record) for tab_record in self.search([])]
        return tabs
