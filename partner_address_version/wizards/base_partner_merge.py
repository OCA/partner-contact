# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from odoo.exceptions import ValidationError


class MergePartnerAutomatic(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    def _get_fk_on_address_version(self, foreign_keys):
        impacted_tables = self.env["res.partner"]._version_impacted_tables()
        excluded_keys = self.env["res.partner"]._version_exclude_keys()
        impacted_columns = self.env["res.partner"]._version_impacted_columns()
        if (impacted_tables or excluded_keys) and impacted_columns:
            raise ValidationError(
                _(
                    "Address versioning error, you must "
                    "exclusively do ONE of the following:"
                    "\n- specify impacted tables and/or excluded keys"
                    "\n- specify impacted columns"
                )
            )
        if impacted_tables or excluded_keys:
            limited_fk = []
            for fk in foreign_keys:
                if fk[0] in impacted_tables:
                    ignore_col = excluded_keys.get(fk[0], False)
                    if ignore_col and fk[1] in ignore_col:
                        continue
                    limited_fk.append(fk)
            return limited_fk
        else:
            return self.env["res.partner"]._version_impacted_columns()

    def _get_fk_on(self, table):
        foreign_keys = super(MergePartnerAutomatic, self)._get_fk_on(table)
        if table == "res_partner" and self.env.context.get("address_version"):
            return self._get_fk_on_address_version(foreign_keys)
        return foreign_keys
