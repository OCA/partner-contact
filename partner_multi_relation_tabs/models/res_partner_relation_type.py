# Copyright 2014-2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# pylint: disable=no-self-use
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerRelationType(models.Model):
    # pylint: disable=too-few-public-methods
    _inherit = 'res.partner.relation.type'

    tab_left_id = fields.Many2one(
        comodel_name='res.partner.tab',
        string='Tab for this relation',
        help="Tab in which these relations will be visible on partner.")
    tab_right_id = fields.Many2one(
        comodel_name='res.partner.tab',
        string='Tab for inverse relation',
        help="Tab in which inverse relations will be visible on partner.")

    @api.multi
    @api.constrains(
        'contact_type_left',
        'partner_category_left',
        'tab_left_id')
    def _check_tab_left(self):
        """Conditions for left partner should be consistent with tab."""
        for rec in self:
            if not rec.tab_left_id:
                continue
            tab_contact_type = rec.tab_left_id.contact_type
            if tab_contact_type and tab_contact_type != rec.contact_type_left:
                raise ValidationError(_(
                    "Contact type left not compatible with left tab"))
            tab_partner_category_id = rec.tab_left_id.partner_category_id
            if tab_partner_category_id and \
                    tab_partner_category_id != rec.partner_category_left:
                raise ValidationError(_(
                    "Partner category left not compatible with left tab"))

    @api.multi
    @api.constrains(
        'contact_type_right',
        'partner_category_right',
        'tab_right_id')
    def _check_tab_right(self):
        """Conditions for right partner should be consistent with tab."""
        for rec in self:
            if not rec.tab_right_id:
                continue
            tab_contact_type = rec.tab_right_id.contact_type
            if tab_contact_type and tab_contact_type != rec.contact_type_right:
                raise ValidationError(_(
                    "Contact type right not compatible with right tab"))
            tab_partner_category_id = rec.tab_right_id.partner_category_id
            if tab_partner_category_id and \
                    tab_partner_category_id != rec.partner_category_right:
                raise ValidationError(_(
                    "Partner category right not compatible with right tab"))
