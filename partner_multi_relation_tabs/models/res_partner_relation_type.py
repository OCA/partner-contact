# -*- coding: utf-8 -*-
# © 2014-2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
TAB_LEFT = 'left'
TAB_RIGHT = 'right'


class ResPartnerRelationType(models.Model):
    _inherit = 'res.partner.relation.type'

    own_tab_left = fields.Boolean('Show in own tab', default=False)
    own_tab_right = fields.Boolean('Show in own tab', default=False)

    def _update_res_partner_fields(self):
        field_name_prefix = 'relation_ids_own_tab_'
        field_name_format = field_name_prefix + '%s_%s'
        res_partner = self.env['res.partner']
        for field_name in res_partner._fields.copy():
            if field_name.startswith(field_name_prefix):
                del res_partner._fields[field_name]

        def add_field(relation, _tab):
            field = fields.One2many(
                'res.partner.relation',
                '%s_partner_id' % (_tab),
                domain=[('type_id.id', '=', relation.id)],
                string=relation['name' if _tab == TAB_LEFT
                                else 'name_inverse'],
                )
            field_name = field_name_format % (relation.id, _tab)
            res_partner._add_field(field_name, field)
        for relation in self.sudo().search(
            ['|',
             ('own_tab_left', '=', True),
             ('own_tab_right', '=', True),
             ]):
            if relation.own_tab_left:
                add_field(relation, TAB_LEFT)
            if relation.own_tab_right:
                add_field(relation, TAB_RIGHT)

    def _register_hook(self):
        self._update_res_partner_fields()

    @api.model
    def create(self, vals):
        result = super(ResPartnerRelationType, self).create(vals)
        if vals.get('own_tab_left') or vals.get('own_tab_right'):
            self._update_res_partner_fields()
        return result

    @api.multi
    def write(self, vals):
        result = super(ResPartnerRelationType, self).write(vals)
        for record in self:
            if 'own_tab_left' in vals or 'own_tab_right' in vals:
                record._update_res_partner_fields()
        return result
