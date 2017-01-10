# -*- coding: utf-8 -*-
# Copyright 2012 Camptocamp SA - Yannick Vaucher
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResPartner(models.Model):
    """Add relation affiliate_ids."""
    _inherit = "res.partner"

    child_ids = fields.One2many(domain=[('is_company', '=', False)])
    affiliate_ids = fields.One2many(
        comodel_name='res.partner',
        inverse_name='parent_id',
        string='Affiliates',
        domain=[('is_company', '=', True)],
    )
