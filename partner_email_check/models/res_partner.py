# -*- coding: utf-8 -*-
import logging
from odoo import api, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    from validate_email import validate_email
except ImportError:
    _logger.debug('Cannot import "validate_email".')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('email')
    def constrains_email(self):
        for rec in self:
            self.email_check(rec.email)

    @api.model
    def email_check(self, email):
        if validate_email(email):
            return True
        else:
            raise UserError(_('Invalid e-mail!'))
