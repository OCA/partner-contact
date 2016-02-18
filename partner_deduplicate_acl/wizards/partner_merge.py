# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID, api, models


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    @api.cr_uid_context
    def _merge(self, cr, uid, partner_ids, dst_partner=None, context=None):
        """Allow non-admins to merge partners with different emails."""
        # Know if user has unrestricted access
        group_unrestricted = self.pool["ir.model.data"].xmlid_to_object(
            cr, uid, "crm_deduplicate_acl.group_unrestricted", context)
        user = self.pool["res.users"].browse(cr, uid, uid, context)

        # Run as admin if so
        return super(BasePartnerMergeAutomaticWizard, self)._merge(
            cr,
            SUPERUSER_ID if group_unrestricted in user.groups_id else uid,
            partner_ids,
            dst_partner,
            context)
