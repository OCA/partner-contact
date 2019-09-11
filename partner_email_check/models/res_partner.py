# -*- coding: utf-8 -*-
# Copyright 2017 Komit <http://komit-consulting.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import api, models, tools, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

try:
    from email_validator import validate_email, EmailNotValidError
except ImportError:
    _logger.debug('Cannot import "email_validator".')

    validate_email = None


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def email_check(self, emails):
        return ','.join(self._normalize_email(email.strip())
                        for email in emails.split(','))

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
        except EmailNotValidError as e:
            raise ValidationError(
                _("%s is an invalid email: %s") % (email.strip(), e.message)
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

    def _validate_no_duplicates(self, email):
        is_existing_record = bool(self)
        if is_existing_record:
            self.ensure_one()

        if is_existing_record and email == self.email:
            # No change, no need to check
            return

        if ',' in email:
            raise ValidationError(
                _("Field contains multiple email addresses. This is not "
                  "supported when duplicate email addresses are not allowed.")
            )

        domain = [('email', '=', email)]
        if is_existing_record:
            domain.append(('id', '!=', self.id))
        if self.search(domain, limit=1):
            raise ValidationError(_("Email '%s' is already in use.") % email)

    @api.model
    def create(self, vals):
        if vals.get('email', False):
            vals['email'] = self.email_check(vals['email'])
            if self._should_filter_duplicates():
                self._validate_no_duplicates(vals['email'])
        return super(ResPartner, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('email', False):
            vals['email'] = self.email_check(vals['email'])
            if self._should_filter_duplicates():
                self._validate_no_duplicates(vals['email'])
        return super(ResPartner, self).write(vals)
