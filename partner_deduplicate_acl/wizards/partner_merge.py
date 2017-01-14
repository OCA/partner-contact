# -*- coding: utf-8 -*-
# © 2016 Tecnativa, S.L. - Jairo Llopis
# © 2016 Tecnativa, S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID, models


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    def _merge(self, cr, uid, partner_ids, dst_partner=None, context=None):
        """Allow non-admins to merge partners"""

        user = self.pool["res.users"].browse(cr, uid, uid, context=context)
        return super(BasePartnerMergeAutomaticWizard, self)._merge(
            cr,
            SUPERUSER_ID if user.has_group(
                'crm_deduplicate_acl.group_unrestricted') else uid,
            partner_ids,
            dst_partner=dst_partner,
            context=context
        )
