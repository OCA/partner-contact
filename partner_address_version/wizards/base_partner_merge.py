# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class MergePartnerAutomatic(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    def _get_fk_on(self, table):
        foreign_keys = super(MergePartnerAutomatic, self)._get_fk_on(table)
        if table == "res_partner" and self.env.context.get("address_version"):
            return self.env["res.partner"]._version_impacted_columns()
        return foreign_keys
