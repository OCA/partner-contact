# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    route_ids = fields.One2many(
        comodel_name="partner.route.item",
        inverse_name="partner_id",
    )
