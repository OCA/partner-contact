# -*- coding: utf-8 -*-
# Copyright 2013-2014 Savoir-faire Linux
#   (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    extension = fields.Char('Extension', help="Phone Number Extension.")
