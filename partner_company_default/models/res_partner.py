# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools import config


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model_create_multi
    def create(self, vals_list):
        # Deliberately a create() override rather than a default on
        # ``company_id``: a field default is applied whenever the key is
        # missing from the values, even when the company is being assigned
        # some other way. With OCA's base_multi_company installed,
        # ``company_id`` becomes a computed field whose inverse *replaces*
        # the real ``company_ids``, so the default silently stomped any
        # explicit ``company_ids`` passed to create() (and, under
        # test_enable, wiped it entirely, as the guard's False still
        # counted as an assigned value). Only fill the company when no
        # company information was provided at all.
        if self._apply_company_default():
            for vals in vals_list:
                if not vals.get("company_id") and not vals.get("company_ids"):
                    vals["company_id"] = self.env.company.id
        return super().create(vals_list)

    @api.model
    def _apply_company_default(self):
        """Skip when creating a company's own partner or for other tests."""
        context = self.env.context
        return not (
            context.get("creating_from_company")
            or config["test_enable"]
            and not context.get("test_partner_company_default")
        )
