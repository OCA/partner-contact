# Copyright 2016 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.tools import SQL


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    exclude_is_company = fields.Boolean("'Is a company?' field selected")
    exclude_not_parent = fields.Boolean("Parent company not set")
    exclude_parent = fields.Boolean("Parent company set (Contacts)")

    def _process_query(self, query):
        if any([self.exclude_is_company, self.exclude_not_parent, self.exclude_parent]):
            filters = []
            if self.exclude_is_company:
                filters.append("is_company = False")
            if self.exclude_not_parent:
                filters.append("parent_id IS NOT NULL")
            if self.exclude_parent:
                filters.append("parent_id IS NULL")
            code, params, to_flush = query._sql_tuple
            index_where = code.find("WHERE")
            index_group_by = code.find("GROUP BY")
            subquery = " AND ".join(filters)
            if index_where > 0 and code[index_where + 5 : index_group_by].strip():
                subquery = f"AND ({subquery}) "
            elif index_where > 0:  # pragma: no cover
                subquery = f"{subquery} "
            else:  # pragma: no cover
                subquery = f"WHERE {subquery} "
            code = code[:index_group_by] + subquery + code[index_group_by:]
            query = SQL(code, *params, to_flush=to_flush)  # pylint: disable=sql-injection
        return super()._process_query(query)
