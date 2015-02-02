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

{
    'name': 'Partner Email Validation',
    'version': '1.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'Customer Relationship Management',
    'summary': 'Validate Partner Email',
    'description': """
    This module performs simple validation on email addresses. Emails are
    checked for:
    - Having a mailbox and domain part: mailbox@domain
    - Having a seemingly valid domain
    - (sub.)*domain.tld where tld has at least two letters
    - @test and @localhost
    - Containing letters or numbers, with a few special characters:
    - ".-_+" for mailbox part
    - "-." for domain part
    - Quoted mailboxes "Foo Bar"@spam.eggs are not supported as of now.

    No email is sent for validation.

    Contributors
    ------------
    * Vincent Vinet (vincent.vinet@savoirfairelinux.com)
    """,
    'depends': [
        'base',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
