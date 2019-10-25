# Copyright 2019 Komit <https://komit-consulting.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import api, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import config

_logger = logging.getLogger(__name__)

try:
    from email_validator import (
        validate_email,
        EmailSyntaxError,
        EmailUndeliverableError,
    )
except ImportError:
    _logger.debug('Cannot import "email_validator".')

    validate_email = None


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def email_check(self, emails):
        if (config['test_enable'] and
                not self.env.context.get('test_partner_email_check')):
            return emails
        return ','.join(self._normalize_email(email.strip())
                        for email in emails.split(','))

    @api.constrains('email')
    def _check_email_unique(self):
        if self._should_filter_duplicates():
            for rec in self.filtered("email"):
                if ',' in rec.email:
                    raise UserError(
                        _("Field contains multiple email addresses. This is "
                          "not supported when duplicate email addresses are "
                          "not allowed.")
                    )
                if self.search_count(
                    [('email', '=', rec.email), ('id', '!=', rec.id)]
                ):
                    raise UserError(
                        _("Email '%s' is already in use.") % rec.email.strip()
                    )

    def _normalize_email(self, email):
        if validate_email is None:
            _logger.warning(
                'Can not validate email, '
                'python dependency required "email_validator"')
            return email

        try:
            result = validate_email(
                email,
                check_deliverability=self._should_check_deliverability(),
            )
        except EmailSyntaxError:
            raise ValidationError(
                _("%s is an invalid email") % email.strip()
            )
        except EmailUndeliverableError:
            raise ValidationError(
                _("Cannot deliver to email address %s") % email.strip()
            )
        return result['local'].lower() + '@' + result['domain_i18n']

    def _should_filter_duplicates(self):
        conf = self.env['ir.config_parameter'].get_param(
            'partner_email_check_filter_duplicates', 'False'
        )
        return conf == 'True'

    def _should_check_deliverability(self):
        conf = self.env['ir.config_parameter'].get_param(
            'partner_email_check_check_deliverability', 'False'
        )
        return conf == 'True'

    @api.model
    def create(self, vals):
        if vals.get('email'):
            vals['email'] = self.email_check(vals['email'])
        return super(ResPartner, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('email'):
            vals['email'] = self.email_check(vals['email'])
        return super(ResPartner, self).write(vals)
