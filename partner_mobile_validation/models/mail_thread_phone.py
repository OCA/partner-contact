# Copyright 2026 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class MailThreadPhone(models.AbstractModel):
    _inherit = "mail.thread.phone"

    mobile_sanitized = fields.Char(compute="_compute_mobile_sanitized", store=True)
    mobile_formatted = fields.Char(
        compute="_compute_mobile_formatted",
    )

    @api.model
    def _phone_get_phone_mobile_search_fields(self):
        phone_fields = super()._phone_get_phone_mobile_search_fields()
        mobile_fields = [
            fname
            for fname in self._mobile_get_number_fields()
            if fname in self._fields and self._fields[fname].store
        ]
        mobile_fields.append("mobile_sanitized")
        return phone_fields + mobile_fields

    @api.depends(lambda self: self._mobile_get_sanitize_triggers())
    def _compute_mobile_sanitized(self):
        number_fields = self._mobile_get_number_fields()
        for record in self:
            sanitized = False
            for fname in number_fields:
                sanitized = record._phone_format(fname=fname)
                if sanitized:
                    break
            record.mobile_sanitized = sanitized

    @api.depends("mobile_sanitized")
    def _compute_mobile_formatted(self):
        for record in self:
            mobile_formatted = record._phone_get_formatted(record.mobile_sanitized)
            record.mobile_formatted = mobile_formatted

    def _mobile_get_sanitize_triggers(self):
        trigger_fields = self._mobile_get_number_fields()
        if trigger_fields:
            country_field = self._phone_get_country_field()
            if country_field:
                trigger_fields.append(country_field)
            trigger_fields += [
                fname
                for fname in self._mail_get_partner_fields()
                if self._fields[fname].store
            ]
        return trigger_fields
