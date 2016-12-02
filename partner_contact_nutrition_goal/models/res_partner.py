# -*- coding: utf-8 -*-
# Copyright 2016 Ursa Information Systems <http://ursainfosystems.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    weight_goal = fields.Selection([('lose', 'Lose weight'),
                                    ('maintain', 'Maintain weight'),
                                    ('gain', 'Gain weight')], "Goal")
