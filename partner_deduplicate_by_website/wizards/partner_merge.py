# Copyright 2016 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    group_by_website = fields.Boolean("Website")

    def _generate_query(self, fields, maximum_group=100):
        """Inject the additional criteria 'website IS NOT NULL' when needed.
        There's no better way to do it, as there are no hooks for adding
        this criteria regularly.
        """
        query = super(BasePartnerMergeAutomaticWizard, self)._generate_query(
            fields, maximum_group=maximum_group
        )
        if "website" in fields:
            if "WHERE" in query:
                index = query.find("WHERE")
                query = (
                    query[: index + 6] + "website IS NOT NULL AND " + query[index + 6 :]
                )
            else:
                index = query.find(" GROUP BY")
                query = query[:index] + " WHERE website IS NOT NULL" + query[index:]
        return query
