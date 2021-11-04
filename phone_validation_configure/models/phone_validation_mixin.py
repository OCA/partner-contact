# Copyright (c) 2004-2015 Odoo S.A.
# Copyright 2021 Le Filament (https://le-filament.com)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html)

from odoo import models

from odoo.addons.phone_validation.tools import phone_validation


class PhoneValidationMixin(models.AbstractModel):
    _inherit = "phone.validation.mixin"

    def phone_format(self, number, country=None, company=None):
        country = country or self._phone_get_country()
        if not country:
            return number
        get_param = self.env["ir.config_parameter"].sudo().get_param
        phone_validation_format = get_param("phone_validation_format")
        phone_validation_exception = get_param("phone_validation_exception")
        return phone_validation.phone_format(
            number,
            country.code if country else None,
            country.phone_code if country else None,
            force_format=phone_validation_format,
            raise_exception=phone_validation_exception,
        )
