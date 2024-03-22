# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class MergePartnerAutomatic(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    def _get_fk_on(self, table):
        foreign_keys = super(MergePartnerAutomatic, self)._get_fk_on(table)
        if table == "res_partner" and self.env.context.get("address_version"):
            models = self.env["res.partner"]._version_impacted_tables()
            limited_fk = []
            for fk in foreign_keys:
                if fk[0] in models:
                    ignore_col_dict = self.env["res.partner"]._version_exclude_keys()
                    ignore_col = ignore_col_dict.get(fk[0], False)
                    if ignore_col and fk[1] in ignore_col:
                        continue
                    limited_fk.append(fk)
            return limited_fk
        return foreign_keys
