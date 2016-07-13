# -*- coding: utf-8 -*-
# © 2016 Tecnativa, S.L. - Jairo Llopis
# © 2016 Tecnativa, S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    @api.model
    def _merge(self, partner_ids, dst_partner=None):
        """Allow non-admins to merge partners with different emails."""
        # Know if user has unrestricted access
        if self.env.user.has_group('crm_deduplicate_acl.group_unrestricted'):
            # Run as admin if so
            self = self.sudo()
        return super(BasePartnerMergeAutomaticWizard, self)._merge(
            partner_ids=partner_ids, dst_partner=dst_partner
        )
