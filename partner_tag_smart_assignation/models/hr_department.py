# Copyright (C) 2019 Compassion CH (http://www.compassion.ch)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResPartnerCategoryExtension(models.Model):
    _inherit = "hr.department"

    tag_ids = fields.Many2many("res.partner.category")
