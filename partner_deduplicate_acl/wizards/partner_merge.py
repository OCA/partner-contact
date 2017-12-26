# Copyright 2016 Tecnativa - Jairo Llopis
# Copyright 2016 Tecnativa - Vicent Cubells
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    def _merge(self, partner_ids, dst_partner=None):
        """Perform the operation as admin if you have unrestricted merge
        rights to avoid the rise of exceptions. An special context key is
        passed for preserving the message author.
        """
        if self.env.user.has_group('crm_deduplicate_acl.group_unrestricted'):
            obj = self.sudo().with_context(message_post_user=self.env.uid)
            if dst_partner:
                dst_partner = dst_partner.with_context(
                    message_post_user=self.env.uid,
                )
        else:
            obj = self
        return super(BasePartnerMergeAutomaticWizard, obj)._merge(
            partner_ids, dst_partner=dst_partner,
        )
