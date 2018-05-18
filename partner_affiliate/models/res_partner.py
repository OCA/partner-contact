# -*- coding: utf-8 -*-
# Copyright 2012 Camptocamp SA - Yannick Vaucher
# Copyright 2018 brain-tec AG - Raul Martin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ResPartner(models.Model):
    """Add relation affiliate_ids."""
    _inherit = "res.partner"

    type = fields.Selection(selection_add=[('affiliate', 'Affiliate')])

    # force "active_test" domain to bypass _search() override
    child_ids = fields.One2many('res.partner', 'parent_id',
                                string='Contacts',
                                domain=[('active', '=', True),
                                        ('is_company', '=', False)])

    # force "active_test" domain to bypass _search() override
    affiliate_ids = fields.One2many('res.partner', 'parent_id',
                                    string='Affiliates',
                                    domain=[('active', '=', True),
                                            ('is_company', '=', True)])
