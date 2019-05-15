# -*- coding: utf-8 -*-
# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, _


class MergePartnerAutomatic(models.TransientModel):
    _inherit = 'base.partner.merge.automatic.wizard'

    def _merge(self, partner_ids, dst_partner=None):
        super(MergePartnerAutomatic, self).sudo(self.user.id).with_context(
            merge_with_original_user_id=self.env.uid
        )._merge(self, partner_ids, dst_partner)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def message_post(self, body, subject, message_type, subtype,
                     parent_id, attachments, content_subtype, **kwargs):
        if self.env.context.get('merge_with_original_user_id'):
            body += _("\n\nMerge processed by {}.".format(self.env.user.name))
        return super(ResPartner, self).message_post(
            body, subject, message_type, subtype, parent_id,
            attachments, content_subtype, **kwargs
        )
