# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerBank(models.Model):

    _name = 'res.partner.bank'
    _inherit = [
        'res.partner.bank',
        'mail.thread',
    ]

    acc_number = fields.Char(
        track_visibility='on_change',
    )
    bank_id = fields.Many2one(
        track_visibility='on_change',
    )
    currency_id = fields.Many2one(
        track_visibility='on_change',
    )
    partner_id = fields.Many2one(
        track_visibility='on_change',
    )
