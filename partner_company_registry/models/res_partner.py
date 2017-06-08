# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_registry = fields.Char(string="Company Registry")
