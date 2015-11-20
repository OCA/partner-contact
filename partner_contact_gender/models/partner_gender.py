# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _, api
from openerp.osv import expression


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('other', 'Other')
                               ])
