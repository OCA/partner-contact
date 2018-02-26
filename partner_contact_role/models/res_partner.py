# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    role_ids = fields.Many2many(
        string='Roles',
        comodel_name='res.partner.role',
    )


class ResPartnerRole(models.Model):

    _name = 'res.partner.role'
    _description = 'Partner Role'

    name = fields.Char()
