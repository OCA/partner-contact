# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2016 Tecnativa S.L. - Pedro M. Baeza
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# Copyright 2019 Tecnativa - Cristina Martin R.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models


class ResPartnerIndustry(models.Model):
    _inherit = "res.partner.industry"
    _order = "parent_path"
    _parent_order = "name"
    _parent_store = True

    name = fields.Char(required=True)
    parent_id = fields.Many2one(
        comodel_name="res.partner.industry", ondelete="restrict"
    )
    child_ids = fields.One2many(
        comodel_name="res.partner.industry", inverse_name="parent_id", string="Children"
    )
    parent_path = fields.Char(index=True)

    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [cat.name, cat.parent_id.name, ...] """
            res = []
            while cat:
                res.insert(0, cat.name)
                cat = cat.parent_id
            return res

        return [(cat.id, " / ".join(get_names(cat))) for cat in self]

    @api.constrains("parent_id")
    def _check_parent_id(self):
        if not self._check_recursion():
            raise exceptions.ValidationError(
                _("Error! You cannot create recursive industries.")
            )
