# -*- coding: utf-8 -*-
# Copyright 2018 Humanitarian Logistics Organisation e.V. - Stefan Becker
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    """Add social media fields"""
    _inherit = "res.partner"

    facebook = fields.Char()
    twitter = fields.Char()
    skype = fields.Char()
    linkedin = fields.Char()
    mastodon = fields.Char()
