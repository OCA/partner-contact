# -*- coding: utf-8 -*-
# Copyright 2017 Oy Tawasta OS Technologies Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    business_id = fields.Char('Business id')
