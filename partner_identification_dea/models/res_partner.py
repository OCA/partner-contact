# Copyright (C) 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


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
        string="Medical License",
        compute="_compute_dea_medical_license",
        store=True,
    )
    medical_license_expired_date = fields.Date(
        string="Medical License Expiration Date",
        compute="_compute_dea_medical_license",
        store=True,
    )

    @api.depends("id_numbers")
    def _compute_dea_medical_license(self):
        dea_category_id = self.env.ref(
            "partner_identification_dea.res_partner_id_category_dea",
            raise_if_not_found=False,
        )
        medical_id = self.env.ref(
            "partner_identification_dea.res_partner_id_category_medical",
            raise_if_not_found=False,
        )
        partner_id_number_obj = self.env["res.partner.id_number"]
        for rec in self:
            dea_number = partner_id_number_obj.search(
                [
                    ("category_id", "=", dea_category_id and dea_category_id.id),
                    ("status", "=", "open"),
                    ("partner_id", "=", rec.id),
                ],
                order="id desc",
                limit=1,
            )
            medical_license = partner_id_number_obj.search(
                [
                    ("category_id", "=", medical_id and medical_id.id),
                    ("status", "=", "open"),
                    ("partner_id", "=", rec.id),
                ],
                order="id desc",
                limit=1,
            )
            rec.dea_active = dea_number and "yes" or "no"
            rec.dea_expired_date = dea_number and dea_number.valid_until or False
            rec.dea_number = dea_number and dea_number.name or ""
            if rec.child_ids and dea_number:
                rec.child_ids.sudo().write({"dea_number": dea_number.name})
            rec.medical_license = medical_license and medical_license.name or ""
            rec.medical_license_expired_date = (
                medical_license and medical_license.valid_until or False
            )

    @api.model
    def send_expiration_date_notification(self):
        """Method is used to send Notification Exiration Date of
        Medical License and DEA Number.
        """
        email_dea_template_id = self.env.ref(
            "partner_identification_dea.email_template_dea_notification",
            raise_if_not_found=False,
        )
        email_medical_template_id = self.env.ref(
            "partner_identification_dea.email_template_medical_notification",
            raise_if_not_found=False,
        )
        des_partner_ids = self.search(
            [
                ("dea_expired_date", "=", fields.Date.today() + relativedelta(days=30)),
                ("dea_active", "=", "yes"),
            ]
        )
        medical_partner_ids = self.search(
            [
                (
                    "medical_license_expired_date",
                    "=",
                    fields.Date.today() + relativedelta(days=30),
                )
            ]
        )
        for partner in des_partner_ids:
            email_dea_template_id.send_mail(
                partner.id,
                force_send=True,
            )

        for partner in medical_partner_ids:
            email_medical_template_id.send_mail(
                partner.id,
                force_send=True,
            )
