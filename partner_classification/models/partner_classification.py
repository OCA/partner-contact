# Copyright 2024 Trobz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class PartnerClassification(models.Model):
    _name = "partner.classification"

    name = fields.Char(required=True)
    parent_id = fields.Many2one(
        "partner.classification", "Parent", index=True, ondelete="cascade"
    )

    @api.constrains("parent_id")
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValueError(_("Error! You cannot create recursive classifications."))
