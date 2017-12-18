# -*- coding: utf-8 -*-
# Copyright 2017 Komit <http://komit-consulting.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import api, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    from validate_email import validate_email
except ImportError:
    _logger.error('Cannot import "validate_email".')

    def validate_email(email):
        _logger.warning(
            'Can not validate email, '
            'python dependency required "validate_email"')
        return True


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('email')
    def constrains_email(self):
        for rec in self.filtered("email"):
            self.email_check(rec.email)

    @api.model
    def email_check(self, email):
        if validate_email(email):
            return True
        else:
            raise UserError(_('Invalid e-mail!'))
