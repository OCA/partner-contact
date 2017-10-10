# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def find_current_relation(self, left, type_relation, right):
        par_rel_mod = self.env['res.partner.relation']
        return par_rel_mod.search([
            ('left_partner_id', '=', left),
            ('type_id', '=', type_relation),
            ('right_partner_id', '=', right)
        ])

    # called without parameters only from the init hook
    def update_relations(self, old_parent_id=None, parent_id=None):
        par_rel_mod = self.env['res.partner.relation']
        type_relation = self.env.ref(
            'partner_multi_relation_parent.parent_relation_type'
        ).id
        for this in self:
            if not parent_id:
                parent_id = this.parent_id.id
            if not old_parent_id:
                old_parent_id = this.parent_id.id
            # unlink previous relation
            if old_parent_id:
                previous = self.find_current_relation(
                    this.id, type_relation, old_parent_id
                )
                previous.unlink()
            # create new relations
            par_rel_mod.create({
                'left_partner_id': this.id,
                'type_id': type_relation,
                'right_partner_id': parent_id,
            })

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals=vals)
        if "parent_id" in vals:
            res.update_relations(None, vals['parent_id'])
        return res

    @api.multi
    def write(self, vals):
        for this in self:
            if this.env.context.get('no_relation_update'):
                continue
            if vals.get('parent_id'):
                this.update_relations(this.parent_id.id, vals['parent_id'])
        res = super(ResPartner, self).write(vals=vals)
        return res
