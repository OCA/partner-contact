# -*- coding: utf-8 -*-
from openerp import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    documents_count = fields.Integer(compute="_compute_nb_related_documents")

    @api.multi
    def _compute_nb_related_documents(self):
        for partner in self:
            partner.documents_count = self.env['signature.request'].search_count(
                [('request_item_ids.partner_id', '=', partner.id)])
