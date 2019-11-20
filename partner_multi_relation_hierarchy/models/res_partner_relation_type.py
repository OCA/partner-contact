# -*- coding: utf-8 -*-
# Copyright 2017-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


HIERARCHY_SELECTION = [
    ('left', 'left_above_right'),
    ('equal', 'equal'),
    ('right', 'right_above_left')]


class ResPartnerRelationType(models.Model):
    _inherit = 'res.partner.relation.type'

    hierarchy = fields.Selection(
        selection=HIERARCHY_SELECTION,
        string='Partners equal, right above, or left above',
        default='equal',
        help="Select wether the relation between the partners"
             " can be considered hierarchical. And if so"
             " which side is considered 'above'.")
