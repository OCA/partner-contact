# Copyright 2017-2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerBank(models.Model):

    _inherit = 'res.partner.bank'

    active = fields.Boolean(default=True)
