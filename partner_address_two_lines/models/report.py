# -*- coding: utf-8 -*-
# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Report(models.Model):
    _inherit = "report"

    @api.multi
    def render(self, template, values=None):
        """ Set context key to split partner address on two line only on report
        """
        if values is not None and 'docs' in values:
            values['docs'] = values.get('docs').with_context(
                _two_lines_partner_address=True
            )

        return super(Report, self).render(template, values)
