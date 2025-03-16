# Copyright 2025 Noviat.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    @api.model
    def _update_foreign_keys(self, src_partners, dst_partner):
        """
        This method will add all id_numbers O2M entries from src_partners to
        the dst_partner record which may result in a raise ValidationError
        'This res.partner has multiple IDs of this type', cf. _inverse_identification.
        We fix this by removing those duplicates.
        """
        res = super()._update_foreign_keys(src_partners, dst_partner)
        id_numbers = dst_partner.id_numbers
        for categ in id_numbers.mapped("category_id"):
            categ_id_numbers = id_numbers.filtered(lambda r: r.category_id == categ)
            if len(categ_id_numbers) > 1:
                categ_id_numbers.sorted(key="id")[1:].unlink()
        return res
