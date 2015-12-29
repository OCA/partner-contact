# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    region_id = fields.Many2one(
        'res.partner.nuts',
        "Region",
        oldname="region")
    substate_id = fields.Many2one(
        'res.partner.nuts',
        "Substate",
        oldname="substate")
    lbl_region = fields.Char(
        default=_("Region"),
        compute='_labels_get')
    lbl_substate = fields.Char(
        default=_("Substate"),
        compute='_labels_get')

    @api.multi
    @api.depends('country_id')
    def _labels_get(self):
        for s in self:
            s.lbl_region = s.country_id.region_label or _('Region')
            s.lbl_substate = s.country_id.substate_label or _('Substate')

    @api.multi
    @api.onchange("substate_id")
    def _onchange_substate_id(self):
        if self.substate_id.country_id:
            self.country_id = self.substate_id.country_id
        return dict()

    @api.multi
    @api.onchange("region_id")
    def _onchange_region_id(self):
        if self.region_id.country_id:
            self.country_id = self.region_id.country_id
        return dict()

    @api.multi
    @api.onchange("country_id")
    def _onchange_country_id(self):
        """Sensible values and domains for related fields."""
        fields = {"state", "region", "substate"}
        country_domain = ([("country_id", "=", self.country_id.id)]
                          if self.country_id else [])

        domain = dict()
        for field in fields:
            field += "_id"
            if self.country_id and self[field].country_id != self.country_id:
                self[field] = False
            domain[field] = list(country_domain)  # Using list() to copy

        fields.remove("state")
        for field in fields:
            level = self.country_id["%s_level" % field]
            field += "_id"
            if level:
                domain[field].append(("level", "=", level))

        return {
            "domain": domain,
        }
