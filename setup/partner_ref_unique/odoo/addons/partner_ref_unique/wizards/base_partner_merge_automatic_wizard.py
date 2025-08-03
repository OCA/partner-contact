# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    def action_merge(self):
        """Inject context for avoiding the duplicate reference constraint that
        happens when merging one contact with reference in another without
        reference.
        """
        return super(
            BasePartnerMergeAutomaticWizard,
            self.with_context(partner_ref_unique_merging=True),
        ).action_merge()
