# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # When we change the country or the state of the partner, Odoo tries to match
    # a proper pricelist for the country, which will be the first it finds with
    # a country group containing such country. The user could be unaware of this
    # change (that could be right or not) and the partner would be left with a
    # wrong pricelist. So we enable traceability to at least be able to log those
    # changes and give the users the chance to amend them. We could also want to log
    # manual changes overtime.
    property_product_pricelist = fields.Many2one(tracking=True)
