# Copyright 2026 glueckkanja AG
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "many2one.color.mixin"]

    own_many2one_color = fields.Selection(
        selection=[("warning", "Warning"), ("critical", "Critical")],
        string="Color State",
        help="Highlight the name of this contact in selection (many2one) fields: "
        "Warning shows it in yellow, Critical in red. Leave empty to use the "
        "color state of the parent contact.",
    )
    own_many2one_color_message = fields.Text(
        string="Color State Message",
        help="Shown as tooltip on the highlighted selection field.",
    )
    # The effective values read by web_many2one_color: the own color state,
    # or the one inherited from the parent contact.
    many2one_color = fields.Selection(
        string="Effective Color State",
        compute="_compute_many2one_color",
        store=True,
        recursive=True,
        help="The own color state of this contact or, when it has none, "
        "the color state of its parent contact.",
    )
    many2one_color_message = fields.Text(
        string="Effective Color State Message",
        compute="_compute_many2one_color",
        store=True,
        recursive=True,
    )

    @api.depends(
        "own_many2one_color",
        "own_many2one_color_message",
        "parent_id.many2one_color",
        "parent_id.many2one_color_message",
    )
    def _compute_many2one_color(self):
        for partner in self:
            if partner.own_many2one_color:
                partner.many2one_color = partner.own_many2one_color
                partner.many2one_color_message = partner.own_many2one_color_message
            else:
                partner.many2one_color = partner.parent_id.many2one_color
                partner.many2one_color_message = (
                    partner.parent_id.many2one_color_message
                )
