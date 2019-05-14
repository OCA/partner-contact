# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nuts1_id = fields.Many2one(
        comodel_name='res.partner.nuts', domain=[('level', '=', 1)],
        string="NUTS L1")
    nuts2_id = fields.Many2one(
        comodel_name='res.partner.nuts', domain=[('level', '=', 2)],
        string="NUTS L2", oldname="region")
    nuts3_id = fields.Many2one(
        comodel_name='res.partner.nuts', domain=[('level', '=', 3)],
        string="NUTS L3", oldname="substate")
    nuts4_id = fields.Many2one(
        comodel_name='res.partner.nuts', domain=[('level', '=', 4)],
        string="NUTS L4")

    def _onchange_nuts(self, level):
        field = self["nuts%d_id" % level]
        country_id = field.country_id
        state_id = field.state_id
        if country_id and self.country_id != country_id:
            self.country_id = country_id
        if state_id and self.state_id != state_id:
            self.state_id = state_id
        if level > 1:
            parent_id = field.parent_id
            if parent_id:
                nuts_parent_level = 'nuts%d_id' % (level - 1)
                parent_field = self[nuts_parent_level]
                if parent_field != parent_id:
                    self[nuts_parent_level] = parent_id
        result = {}
        if country_id and level < 4:
            result['domain'] = {}
            while level < 4:
                parent_field = 'nuts%d_id' % level
                domain_field = 'nuts%d_id' % (level + 1)
                parent_id = self[parent_field].id
                if parent_id:
                    result['domain'][domain_field] = [
                        ('parent_id', '=', parent_id),
                    ]
                level += 1
        return result

    @api.onchange('nuts4_id')
    def _onchange_nuts4_id(self):
        return self._onchange_nuts(4)

    @api.onchange('nuts3_id')
    def _onchange_nuts3_id(self):
        return self._onchange_nuts(3)

    @api.onchange('nuts2_id')
    def _onchange_nuts2_id(self):
        return self._onchange_nuts(2)

    @api.onchange('nuts1_id')
    def _onchange_nuts1_id(self):
        return self._onchange_nuts(1)

    @api.onchange('country_id')
    def _onchange_country_id_base_location_nuts(self):
        """Sensible values and domains for related fields."""
        fields = ['state_id', 'nuts1_id', 'nuts2_id', 'nuts3_id', 'nuts4_id']
        country_domain = ([('country_id', '=', self.country_id.id)]
                          if self.country_id else [])
        domain = dict()
        for field in fields:
            if self.country_id and self[field].country_id != self.country_id:
                self[field] = False
            domain[field] = list(country_domain)  # Using list() to copy
        fields.remove('state_id')
        for field in fields:
            level = int(field[4])
            domain[field].append(('level', '=', level))
        if self.country_id:
            nuts1 = self.env['res.partner.nuts'].search([
                ('level', '=', 1),
                ('country_id', '=', self.country_id.id),
            ], limit=1)
            if self.nuts1_id.id != nuts1.id:
                self.nuts1_id = nuts1.id
        return {
            'domain': domain,
        }

    @api.onchange('state_id')
    def onchange_state_id_base_location_nuts(self):
        if self.state_id:
            self.country_id = self.state_id.country_id
            if self.state_id.country_id.state_level:
                nuts_state = self.env['res.partner.nuts'].search([
                    ('level', '=', self.state_id.country_id.state_level),
                    ('state_id', '=', self.state_id.id)
                ], limit=1)
                if nuts_state:
                    field = 'nuts%d_id' % self.state_id.country_id.state_level
                    self[field] = nuts_state

    @api.model
    def _address_fields(self):
        fields = super(ResPartner, self)._address_fields()
        if fields:
            fields += ['nuts1_id', 'nuts2_id', 'nuts3_id', 'nuts4_id']
        return fields
