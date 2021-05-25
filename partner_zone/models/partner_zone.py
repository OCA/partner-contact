# Copyright 2021 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PartnerZone(models.Model):
    _name = 'partner.zone'
    _description = 'Partner Zone'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (
                    category.parent_id.complete_name, category.name
                )
            else:
                category.complete_name = category.name

    def name_get(self):
        result = []
        for record in self:
            name = ''
            if record.code:
                name += '[' + record.code + '] '
            if record.zone_type_id:
                name += record.zone_type_id.name + ' / '
            name += record.complete_name
            result.append((record.id, name))
        return result

    code = fields.Char(
        string='Code',
    )

    name = fields.Char(
        string='Name',
        required=True,
        index=True,
        translate=True,
    )

    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        store=True,
    )

    parent_id = fields.Many2one(
        comodel_name='partner.zone',
        string='Parent Zone',
        index=True,
        ondelete='cascade'
    )

    parent_path = fields.Char(
        index=True,
    )

    child_id = fields.One2many(
        comodel_name='partner.zone',
        inverse_name='parent_id',
        string='Child Zones',
    )

    zone_type_id = fields.Many2one(
        string='Zone Type',
        comodel_name='partner.zone.type',
        required=True,
    )

    zone_type = fields.Selection(
        related='zone_type_id.zone_type',
        string='Type',
        readonly=True,
        store=True,
    )

    country_ids = fields.Many2many(
        string='Countries',
        comodel_name='res.country',
    )

    state_ids = fields.Many2many(
        string='States',
        comodel_name='res.country.state',
    )

    city_ids = fields.Many2many(
        string='Cities',
        comodel_name='res.city',
    )

    category_ids = fields.Many2many(
        string='Tags',
        comodel_name='res.partner.category'
    )

    industry_ids = fields.Many2many(
        string='Industries',
        comodel_name='res.partner.industry'
    )

    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='partner_zone_rel',
        column1='zone_id',
        column2='partner_id',
        string='Partners',
    )

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive zones.'))
        return True

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]

    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        if self.parent_id and self.parent_id.zone_type_id:
            self.zone_type_id = self.parent_id.zone_type_id
