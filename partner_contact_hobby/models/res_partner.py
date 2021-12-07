# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    hobby_ids = fields.Many2many(
        "res.partner.hobby",
        "res_partner_hobby_rel",
        "partner_id",
        "hobby_id",
        "Hobbies",
        help="Partner Hobbies",
    )
