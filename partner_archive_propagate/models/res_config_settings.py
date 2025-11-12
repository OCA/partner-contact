# Copyright 2025 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_archive_force_outside_ui = fields.Boolean(
        string="Force propagation outside UI",
        help="If enabled, archiving a partner via any non-UI method (imports, RPC, automated) "
        "will also archive all descendants and mark them as propagated.",
        config_parameter="partner_archive_propagate.force_outside_ui",
        default=False,
    )
