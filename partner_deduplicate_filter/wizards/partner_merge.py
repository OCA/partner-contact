# Copyright 2016 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


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
            index_where = query.find("WHERE")
            index_group_by = query.find("GROUP BY")
            subquery = "%s" % " AND ".join(filters)
            if index_where > 0:
                subquery = "AND (%s) " % subquery
            else:  # pragma: no cover
                subquery = "WHERE %s " % subquery
            query = query[:index_group_by] + subquery + query[index_group_by:]
        return super()._process_query(query)
