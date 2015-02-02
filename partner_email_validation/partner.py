# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
import unicodedata

from openerp.osv import orm
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class Partner(orm.Model):
    _name = _inherit = 'res.partner'

    def _check_email_domain(self, domain):
        """ Checks if a domain is valid for an email """
        # Allow localhost and test, those are valid domains
        if domain in (u'localhost', u'test'):
            return True

        domain_parts = domain.split(u".")

        # Disallow @foo @foo. @foo..com
        if len(domain_parts) <= 1:
            _logger.debug("Email has single domain part")
            return False

        # Disallow @foo. @foo..com, @.b
        for part in domain_parts:
            if not part:
                _logger.debug("Empty domain part")
                return False

        # TLD must have 2 chars at least
        if len(domain_parts[-1]) < 2:
            _logger.debug("TLD too short")
            return False

        # Check that we have letters, numbers, '.' or '-'
        for letter in domain:
            if letter in ".-":
                continue

            cat = unicodedata.category(letter)
            if cat[0] not in u'LN':  # Letter or Number
                _logger.debug("Character not accepted in domain: %r",
                              letter)
                return False

        return True

    def _check_email_mailbox(self, mailbox):
        """ Checks if a mailbox is valid for an email """
        for letter in mailbox:
            if letter in ".-_+":  # Few accepted symbols
                continue

            cat = unicodedata.category(letter)
            if cat[0] not in u'LN':  # Letter or Number
                _logger.debug("Character not accepted in mailbox: %r",
                              letter)
                return False

        return True

    def _check_valid_email(self, email):
        """ Checks if an email address is valid """
        mail, sep, domain = email.rpartition(u'@')
        # We need a full "mail@domain"
        if not mail or not sep or not domain:
            _logger.debug("Mail is not mail@domain")
            return False

        if not self._check_email_domain(domain):
            return False

        if not self._check_email_mailbox(mail):
            return False

        return True

    def _check_customer_email(self, cr, uid, ids, context=None):
        for partner in self.browse(cr, uid, ids, context=None):
            if not partner.email:
                # The view already forces the email to be filled, do not
                # double check or repeat conditions
                continue

            if not self._check_valid_email(partner.email):
                return False

        return True

    _constraints = [
        (_check_customer_email,
         _('You must provide a valid email address'), ['email']),
    ]
