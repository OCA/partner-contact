# -*- coding: utf-8 -*-
# Copyright 2016 Ursa Information Systems <http://ursainfosystems.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    activity_level = fields.Selection([('sedentary', 'Sedentary'),
                                       ('moderately', 'Moderately active'),
                                       ('very', 'Very active'),
                                       ('extremely', 'Extremely active')],
                                      "Activity Level")
