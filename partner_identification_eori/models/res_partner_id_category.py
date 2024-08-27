# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartnerIdCategory(models.Model):
    _inherit = "res.partner.id_category"

    def validate_res_partner_eori(self, id_number):
        self.ensure_one()
        if not id_number:
            return False

        if (
            id_number.partner_id
            and id_number.partner_id.country_id
            and not id_number.name.startswith(id_number.partner_id.country_id.code)
        ):
            return True

        cat = self.env.ref(
            "partner_identification_eori.partner_identification_eori_number_category"
        ).id
        duplicate_eori = self._search_duplicate(cat, id_number, True)

        if duplicate_eori:
            return True

        return False
