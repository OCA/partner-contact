# Copyright 2012 Camptocamp SA - Yannick Vaucher
# Copyright 2018 brain-tec AG - Raul Martin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Modify core's field
    child_ids = fields.One2many(
        # Same than core's, but with is_company == False
        domain=[("active", "=", True), ("is_company", "=", False)]
    )

    affiliate_ids = fields.One2many(
        comodel_name="res.partner",
        inverse_name="parent_id",
        string="Affiliates",
        # Same than core's child_ids, but with is_company == True
        domain=[("active", "=", True), ("is_company", "=", True)],
        context={"active_test": False},
    )
