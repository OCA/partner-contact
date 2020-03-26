# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    group_by_ref = fields.Boolean("Reference")

    def _generate_query(self, fields, maximum_group=100):
        """Inject the additional criteria 'ref IS NOT NULL' when needed.
        There's no better way to do it, as there are no hooks for adding
        this criteria regularly.
        """
        query = super()._generate_query(fields, maximum_group=maximum_group)
        if "ref" in fields:
            if "WHERE" in query:
                index = query.find("WHERE")
                query = query[: index + 6] + "ref IS NOT NULL AND " + query[index + 6 :]
            else:
                index = query.find(" GROUP BY")
                query = query[:index] + " WHERE ref IS NOT NULL" + query[index:]
        return query
