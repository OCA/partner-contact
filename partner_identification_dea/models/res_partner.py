# Copyright (C) 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.fields import Domain


class ResPartner(models.Model):
    _inherit = "res.partner"

    dea_number = fields.Char(
        string="DEA #",
        compute="_compute_dea_medical_license",
        store=True,
    )
    dea_expired_date = fields.Date(
        string="DEA Expiration Date",
        compute="_compute_dea_medical_license",
        store=True,
    )
    dea_active = fields.Selection(
        [("yes", "Yes"), ("no", "NO")],
        string="DEA Active",
        compute="_compute_dea_medical_license",
        store=True,
    )
    medical_license = fields.Char(
        compute="_compute_dea_medical_license",
        store=True,
    )
    medical_license_expired_date = fields.Date(
        string="Medical License Expiration Date",
        compute="_compute_dea_medical_license",
        store=True,
    )
    contr_subst_license = fields.Char(
        string="Contr. Subst. License",
        compute="_compute_dea_medical_license",
        store=True,
    )
    contr_subst_expired_date = fields.Date(
        string="Contr. Subst. Expiration Date",
        compute="_compute_dea_medical_license",
        store=True,
    )

    def _get_open_id_number(self, category):
        self.ensure_one()
        if not category:
            return self.env["res.partner.id_number"]
        return self.id_numbers.filtered(
            lambda number: number.category_id == category and number.status == "open"
        ).sorted("id", reverse=True)[:1]

    @api.depends(
        "id_numbers",
        "id_numbers.name",
        "id_numbers.status",
        "id_numbers.valid_until",
        "id_numbers.category_id",
    )
    def _compute_dea_medical_license(self):
        dea_category = self.env.ref(
            "partner_identification_dea.res_partner_id_category_dea",
            raise_if_not_found=False,
        )
        medical_category = self.env.ref(
            "partner_identification_dea.res_partner_id_category_medical",
            raise_if_not_found=False,
        )
        controlled_category = self.env.ref(
            "partner_identification_dea.res_partner_id_category_controlled_substance",
            raise_if_not_found=False,
        )
        for rec in self:
            dea_number = rec._get_open_id_number(dea_category)
            medical_license = rec._get_open_id_number(medical_category)
            controlled_subst = rec._get_open_id_number(controlled_category)
            rec.dea_active = "yes" if dea_number else "no"
            rec.dea_expired_date = dea_number.valid_until if dea_number else False
            rec.dea_number = dea_number.name if dea_number else ""
            rec.medical_license = medical_license.name if medical_license else ""
            rec.medical_license_expired_date = (
                medical_license.valid_until if medical_license else False
            )
            rec.contr_subst_license = controlled_subst.name if controlled_subst else ""
            rec.contr_subst_expired_date = (
                controlled_subst.valid_until if controlled_subst else False
            )

    @api.model
    def send_expiration_date_notification(self):
        """Send a notification 30 days before a DEA number expires."""
        email_dea_template = self.env.ref(
            "partner_identification_dea.email_template_dea_notification",
            raise_if_not_found=False,
        )
        if not email_dea_template:
            return
        partners = self.search(
            [
                ("dea_expired_date", "=", fields.Date.today() + relativedelta(days=30)),
                ("dea_active", "=", "yes"),
            ]
        )
        for partner in partners:
            email_dea_template.send_mail(partner.id, force_send=True)

    def _search_display_name(self, operator, value):
        domain = super()._search_display_name(operator, value)
        if value and operator in ("=", "ilike", "=ilike", "like", "=like"):
            domain |= Domain("contr_subst_license", operator, value)
        return domain
