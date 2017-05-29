# -*- coding: utf-8 -*-
# © 2017 Sunflower IT <http://sunflowerweb.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api
from ast import literal_eval


class MergePartnerAutomatic(models.TransientModel):
    _inherit = 'base.partner.merge.automatic.wizard'

    # Enable deduplicating by reference
    group_by_ref = fields.Boolean('Reference')

    @api.multi
    def _process_query(self, query):
        ret = super(MergePartnerAutomatic, self)._process_query(query)

        # If 'extra_domain', deduplicate only the records matching the domain
        extra_domain = self.env.context.get('partner_merge_domain', [])
        if extra_domain:
            for line in self.line_ids:
                domain = [('id', 'in', literal_eval(line.aggr_ids))]
                domain.extend(extra_domain)
                aggr_ids = self.env['res.partner'].search(domain).ids
                if len(aggr_ids) > 1:
                    line.aggr_ids = str(aggr_ids)
                else:
                    line.unlink()
        return ret
