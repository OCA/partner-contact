# -*- coding: utf-8 -*-
# Copyright 2017-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _compute_partners_above(self):
        """Check partners up in the hierarchy if any."""
        for this in self:
            this.partner_above_hierarchy = \
                this.partner_above_ids and \
                this.partner_above_ids[0].hierarchy_display or ''
            this.has_partner_above = bool(this.partner_above_ids)

    partner_above_ids = fields.One2many(
        comodel_name='res.partner.relation.hierarchy',
        inverse_name='partner_id',
        string='Partners above in hierarchy',
        readonly=True)
    partner_above_hierarchy = fields.Char(
        string="Upper level partners",
        compute='_compute_partners_above',
        readonly=True)
    has_partner_above = fields.Boolean(
        compute='_compute_partners_above',
        readonly=True)

    @api.multi
    def is_above(self, other_partner):
        """Check whether this partner is above other_partner."""
        self.ensure_one()
        for partner_above in other_partner.partner_above_ids:
            if self.id == partner_above.partner_above_id.id:
                return True
        return False
