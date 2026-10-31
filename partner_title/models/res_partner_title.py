# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerTitle(models.Model):
    _name = "res.partner.title"
    _description = "Title on Partners"
    _order = "sequence, name"
    # This model exists up to Odoo 18.0 and was dropped in 19.0

    name = fields.Char(string="Title", required=True, translate=True)
    shortcut = fields.Char(string="Abbreviation", translate=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer()

    _name_unique = models.Constraint("unique(name)", "This title already exists.")
