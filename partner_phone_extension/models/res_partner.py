# -*- coding: utf-8 -*-
# copyright 2013-2014 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#

from openerp import fields, models


class res_partner(models.Model):
    _inherit = 'res.partner'

    extension = fields.Char('Extension', help="Phone Number Extension.")
