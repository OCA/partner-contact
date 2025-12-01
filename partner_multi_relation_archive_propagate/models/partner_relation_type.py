# Copyright 2025 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerRelationType(models.Model):
    _inherit = "res.partner.relation.type"

    propagate_archive = fields.Boolean(
        string="Propagate archive",
        help=(
            "If enabled, archiving an organisational partner will also archive "
            "partners that are linked through relations of this type, when "
            "they are not linked to active users. Those partners are marked "
            "as propagated, so they can be unarchived again together with the "
            "organisation."
        ),
    )
