# Copyright 2016 Tecnativa - Jairo Llopis
# Copyright 2016 Tecnativa - Vicent Cubells
# Copyright 2017-2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    def _merge(self, partner_ids, dst_partner=None, extra_checks=True):
        """Pass extra_checks=False if we have the extra group for avoiding
        the checks.
        """
        if self.env.user.has_group(
            'partner_deduplicate_acl.group_unrestricted'
        ):
            extra_checks = False
        return super()._merge(
            partner_ids, dst_partner=dst_partner, extra_checks=extra_checks,
        )
