# -*- coding: utf-8 -*-
# RFC 2822 - style email validation for Python
# (c) 2012 Syrus Akbary <me@syrusakbary.com>
# Extended from (c) 2011 Noel Bush <noel@aitools.org>
# for support of mx and user check
# This code is made available to you under the GNU LGPL v3.
#
# This module provides a single method, valid_email_address(),
# which returns True or False to indicate whether a given address
# is valid according to the 'addr-spec' part of the specification
# given in RFC 2822.  Ideally, we would like to find this
# in some other library, already thoroughly tested and well-
# maintained.  The standard Python library email.utils
# contains a parse_addr() function, but it is not sufficient
# to detect many malformed addresses.
#
# This implementation aims to be faithful to the RFC, with the
# exception of a circular definition (see comments below), and
# with the omission of the pattern components marked as "obsolete".

import re
import smtplib

try:
    import DNS
    ServerError = DNS.ServerError
except:
    DNS = None

    class ServerError(Exception):
        pass
# All we are really doing is comparing the input string to one
# gigantic regular expression.  But building that regexp, and
# ensuring its correctness, is made much easier by assembling it
# from the "tokens" defined by the RFC.  Each of these tokens is
# tested in the accompanying unit test file.
#
# The section of RFC 2822 from which each pattern component is
# derived is given in an accompanying comment.
#
# (To make things simple, every string below is given as 'raw',
# even when it's not strictly necessary.  This way we don't forget
# when it is necessary.)
#
WSP = r'[ \t]'
CRLF = r'(?:\r\n)'
NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'
QUOTED_PAIR = r'(?:\\.)'
FWS = r'(?:(?:{0}*{1})?{0}+)'.format(WSP, CRLF)
CTEXT = r'[{0}\x21-\x27\x2a-\x5b\x5d-\x7e]'.format(NO_WS_CTL)
CCONTENT = r'(?:{0}|{1})'.format(CTEXT, QUOTED_PAIR)
COMMENT = r'\((?:{0}?{1})*{0}?\)'.format(FWS, CCONTENT)
CFWS = r'(?:{0}?{1})*(?:{0}?{1}|{0})'.format(FWS, COMMENT)
ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'
ATOM = r'{0}?{1}+{0}?'.format(CFWS, ATEXT)
DOT_ATOM_TEXT = r'{0}+(?:\.{0}+)*'.format(ATEXT)
DOT_ATOM = r'{0}?{1}{0}?'.format(CFWS, DOT_ATOM_TEXT)
QTEXT = r'[{0}\x21\x23-\x5b\x5d-\x7e]'.format(NO_WS_CTL)
QCONTENT = r'(?:{0}|{1})'.format(QTEXT, QUOTED_PAIR)
QUOTED_STRING = r'{0}?"(?:{1}?{2})*{1}?"{0}?'.format(CFWS, FWS, QCONTENT)
LOCAL_PART = r'(?:{0}|{1})'.format(DOT_ATOM, QUOTED_STRING)
DTEXT = r'[{0}\x21-\x5a\x5e-\x7e]'.format(NO_WS_CTL)
DCONTENT = r'(?:{0}|{1})'.format(DTEXT, QUOTED_PAIR)
DOMAIN_LITERAL = r'{0}?\[(?:{1}?{2})*{1}?\]{0}?'.format(CFWS, FWS, DCONTENT)
DOMAIN = r'(?:{0}|{1})'.format(DOT_ATOM, DOMAIN_LITERAL)
ADDR_SPEC = r'{0}@{1}'.format(LOCAL_PART, DOMAIN)
VALID_ADDRESS_REGEXP = '^' + ADDR_SPEC + '$'


def validate_email(email, check_mx=False, verify=False):
    """Indicate whether the given string is a valid email address
    according to the 'addr-spec' portion of RFC 2822 (see section
    3.4.1).  Parts of the spec that are marked obsolete are *not*
    included in this test, and certain arcane constructions that
    depend on circular definitions in the spec may not pass, but in
    general this should correctly identify any email address likely
    to be in use as of 2011."""
    try:
        assert re.match(VALID_ADDRESS_REGEXP, email) is not None
        check_mx |= verify
        if check_mx:
            if not DNS:
                raise Exception('For check the mx records or check if the '
                                'email exists you must have installed pyDNS '
                                'python package')
            DNS.DiscoverNameServers()
            hostname = email[email.find('@') + 1:]
            mx_hosts = DNS.mxlookup(hostname)
            for mx in mx_hosts:
                try:
                    smtp = smtplib.SMTP()
                    smtp.connect(mx[1])
                    if not verify:
                        return True
                    status, _ = smtp.helo()
                    if status != 250:
                        continue
                    smtp.mail('')
                    status, _ = smtp.rcpt(email)
                    if status != 250:
                        return False
                    break
                # Server not permits verify user
                except smtplib.SMTPServerDisconnected:
                    break
                except smtplib.SMTPConnectError:
                    continue
    except (AssertionError, ServerError):
        return False
    return True
