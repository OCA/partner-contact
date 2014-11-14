# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010-2011 Camptocamp SA (http://www.camptocamp.com)
# All Right Reserved
#
# Author : Nicolas Bessi (Camptocamp),
# Thanks to Laurent Lauden for his code adaptation
# Active directory Donor: M. Benadiba (Informatique Assistances.fr)
# Contribution : Joel Grand-Guillaume
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
# TODO Find why company parameter are cached

import re
import unicodedata
from openerp import netsvc
try:
    import ldap
    import ldap.modlist
except:
    print('python ldap not installed please install it in order to use this '
          'module')


from openerp.osv import orm, fields
from openerp.tools.translate import _

logger = netsvc.Logger()


class LdapConnMApper(object):
    """LdapConnMApper: push specific fields from the Terp
    Partner_contacts to the LDAP schema inetOrgPerson. Ldap bind options
    are stored in company.
    """

    def __init__(self, cursor, uid, osv_obj, context=None):
        """Initialize connexion to ldap by using parameter set in the
        current user compagny
        """
        logger.notifyChannel("MY TOPIC", netsvc.LOG_DEBUG,
                             _('Initalize LDAP CONN'))
        self.USER_DN = ''
        self.CONTACT_DN = ''
        self.LDAP_SERVER = ''
        self.PASS = ''
        self.OU = ''
        self.connexion = ''
        self.ACTIVDIR = False

        # Reading ldap pref
        user = osv_obj.pool.get('res.users').browse(
            cursor, uid, uid, context=context
        )
        company = user.company_id
        self.USER_DN = company.base_dn
        self.CONTACT_DN = company.contact_dn
        self.LDAP_SERVER = company.ldap_server
        self.PASS = company.passwd
        self.PORT = company.ldap_port
        self.OU = company.ounit
        self.ACTIVDIR = company.is_activedir

        mand = (
            self.USER_DN,
            self.CONTACT_DN,
            self.LDAP_SERVER,
            self.PASS, self.OU
        )
        if company.ldap_active:
            for param in mand:
                if not param:
                    raise orm.except_orm(
                        _('Warning !'),
                        _('An LDAP parameter is missing for company %s') %
                        (company.name, )
                    )

    def get_connexion(self):
        """create a new ldap connexion"""
        logger.notifyChannel(
            "LDAP Address",
            netsvc.LOG_DEBUG,
            _('connecting to server ldap %s') % (self.LDAP_SERVER, )
        )
        if self.PORT:
            self.connexion = ldap.open(self.LDAP_SERVER, self.PORT)
        else:
            self.connexion = ldap.open(self.LDAP_SERVER)
        self.connexion.simple_bind_s(self.USER_DN, self.PASS)
        return self.connexion


class LDAPAddress(orm.Model):
    """Override the CRUD of the objet in order to dynamically bind to ldap"""
    _inherit = 'res.partner.address'
    ldapMapper = None

    def init(self, cr):
        logger = netsvc.Logger()
        try:
            logger.notifyChannel(
                _('LDAP address init'),
                netsvc.LOG_INFO,
                _('try to ALTER TABLE res_partner_address RENAME '
                  'column name to lastname ;'))
            cr.execute(
                'ALTER TABLE res_partner_address'
                'RENAME column name to lastname ;'
            )

        except Exception:
            cr.rollback()
            logger.notifyChannel(
                _('LDAP address init'),
                netsvc.LOG_INFO,
                _('Warning ! impossible to rename column name into lastname, '
                  'this is probably already done or does not exist')
            )

    def _compute_name(self, firstname, lastname):
        firstname = firstname or u''
        lastname = lastname or u''
        firstname = (u' ' + firstname).rstrip()
        return u"%s%s" % (lastname, firstname)

    def _name_get_fnc(self, cursor, uid, ids, name, arg, context=None):
        """Get the name (lastname + firstname), otherwise ''"""
        if not ids:
            return []
        reads = self.read(cursor, uid, ids, ['lastname', 'firstname'])
        res = []
        for record in reads:
            # We want to have " firstname" or ""
            name = self._compute_name(record['firstname'], record['lastname'])
            res.append((record['id'], name))
        return dict(res)

    # TODO get the new version of name search not vulnerable to sql injections
    # def name_search(
    #         self, cursor, user, name, args=None, operator='ilike',
    #         context=None, limit=100):
    #     if not context: context = {}
    #     prep_name = '.*%s.*' %(name)
    #     cursor.execute(("""
    # select id from res_partner_address where
    # (to_ascii(convert( lastname, 'UTF8', 'LATIN1'),'LATIN-1')  ~* '%s'
    #  or to_ascii(convert( firstname, 'UTF8', 'LATIN1'),'LATIN-1')  ~* '%s')
    #  limit %s""") % (prep_name, prep_name, limit))
    #     res = cursor.fetchall()
    #     if res:
    #         res = [x[0] for x in res]
    #     else:
    #         res = []
    # search in partner name to know if we are searching partner...
    #     partner_obj=self.pool.get('res.partner')
    #     part_len = len(res)-limit
    #     if part_len > 0:
    #         partner_res = partner_obj.search(
    #             cursor, user, [('name', 'ilike', name)],
    #             limit=part_len, context=context
    #         )
    #         for p in partner_res:
    #             addresses = partner_obj.browse(cursor, user, p).address
    # Take each contact and add it to
    #             for add in addresses:
    #                 res.append(add.id)
    #     return self.name_get(cursor, user, res, context)

    _columns = {
        'firstname': fields.char('First name', size=256),
        'lastname': fields.char('Last name', size=256),
        'name': fields.function(
            _name_get_fnc,
            method=True,
            type="char",
            size=512,
            store=True,
            string='Contact Name',
            help='Name generated from the first name and last name',
            nodrop=True
        ),
        'private_phone': fields.char('Private phone', size=128),
    }

    def create(self, cursor, uid, vals, context=None):
        if context is None:
            context = {}
        self.getconn(cursor, uid, {})
        ids = None
        self.validate_entries(vals, cursor, uid, ids)
        tmp_id = super(LDAPAddress, self).create(cursor, uid,
                                                 vals, context)
        if self.ldaplinkactive(cursor, uid, context):
            self.saveLdapContact(tmp_id, vals, cursor, uid, context)
        return tmp_id

    def write(self, cursor, uid, ids, vals, context=None):
        context = context or {}
        self.getconn(cursor, uid, {})
        if not isinstance(ids, list):
            ids = [ids]
        if ids:
            self.validate_entries(vals, cursor, uid, ids)
        if context.get('init_mode'):
            success = True
        else:
            success = super(LDAPAddress, self).write(cursor, uid, ids,
                                                     vals, context)
        if self.ldaplinkactive(cursor, uid, context):
            for address_id in ids:
                self.updateLdapContact(address_id, vals, cursor, uid, context)
        return success

    def unlink(self, cursor, uid, ids, context=None):
        if context is None:
            context = {}
        if ids:
            self.getconn(cursor, uid, {})
            if not isinstance(ids, list):
                ids = [ids]
            if self.ldaplinkactive(cursor, uid, context):
                for id in ids:
                    self.removeLdapContact(id, cursor, uid)
        return super(LDAPAddress, self).unlink(cursor, uid, ids)

    def validate_entries(self, vals, cursor, uid, ids):
        """Validate data of an address based on the inetOrgPerson schema"""
        for val in vals:
            try:
                if isinstance(vals[val], basestring):
                    vals[val] = unicode(vals[val].decode('utf8'))
            except UnicodeError:
                logger.notifyChannel('LDAP encode', netsvc.LOG_DEBUG,
                                     'cannot unicode ' + vals[val])

        if ids is not None:
            if isinstance(ids, (int, long)):
                ids = [ids]
            if len(ids) == 1:
                self.addNeededFields(ids[0], vals, cursor, uid)
        email = vals.get('email', False)
        phone = vals.get('phone', False)
        fax = vals.get('fax', False)
        mobile = vals.get('mobile', False)
        private_phone = vals.get('private_phone', False)
        if email:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\."
                        "([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",
                        email) is None:
                raise orm.except_orm(_('Warning !'),
                                     _('Please enter a valid e-mail'))
        phones = (('phone', phone), ('fax', fax), ('mobile', mobile),
                  ('private_phone', private_phone))
        for phone_tuple in phones:
            phone_number = phone_tuple[1]
            if phone_number:
                if not phone_number.startswith('+'):
                    raise orm.except_orm(
                        _('Warning !'),
                        _('Please enter a valid phone number in %s'
                          ' international format (i.e. leading +)')
                        % phone_tuple[0])

    def getVals(self, att_name, key, vals, dico, uid, ids, cr, context=None):
        """map to values to dict"""
        if not context:
            context = {}
        # We explicitly test False value
        if vals.get(key, False) is not False:
            dico[att_name] = vals[key]
        else:
            if context.get('init_mode'):
                return False
            tmp = self.read(cr, uid, ids, [key], context={})
            if tmp.get(key, False):
                dico[att_name] = tmp[key]

    def _un_unicodize_buf(self, in_buf):
        if isinstance(in_buf, unicode):
            try:
                return in_buf.encode()
            except Exception:
                return unicodedata.normalize("NFKD", in_buf).encode(
                    'ascii', 'ignore'
                )
        return in_buf

    def unUnicodize(self, indict):
        """remove unicode data of modlist as unicode is not supported
        by python-ldap library till version 2.7
        """
        for key in indict:
            if not isinstance(indict[key], list):
                indict[key] = self._un_unicodize_buf(indict[key])
            else:
                nonutfArray = []
                for val in indict[key]:
                    nonutfArray.append(self._un_unicodize_buf(val))
                indict[key] = nonutfArray

    def addNeededFields(self, id, vals, cursor, uid):
        previousvalue = self.browse(cursor, uid, [id])[0]
        if not vals.get('partner_id'):
            vals['partner_id'] = previousvalue.partner_id.id
        values_to_check = ('email', 'phone', 'fax', 'mobile', 'firstname',
                           'lastname', 'private_phone', 'street', 'street2')
        for val in values_to_check:
            if not vals.get(val):
                vals[val] = previousvalue[val]

    def mappLdapObject(self, id, vals, cr, uid, context):
        """Mapp ResPArtner adress to moddlist"""
        self.addNeededFields(id, vals, cr, uid)
        conn = self.getconn(cr, uid, {})
        partner_obj = self.pool.get('res.partner')
        part_name = partner_obj.browse(cr, uid, vals['partner_id']).name
        vals['partner'] = part_name
        name = self._compute_name(vals.get('firstname'), vals.get('lastname'))
        if name:
            cn = name
        else:
            cn = part_name
        if not vals.get('lastname'):
            vals['lastname'] = part_name
        contact_obj = {'objectclass': ['inetOrgPerson'],
                       'uid': ['terp_' + str(id)],
                       'ou': [conn.OU],
                       'cn': [cn],
                       'sn': [vals['lastname']]}
        if not vals.get('street'):
            vals['street'] = u''
        if not vals.get('street2'):
            vals['street2'] = u''
        street_key = 'street'
        if self.getconn(cr, uid, {}).ACTIVDIR:
            # ENTERING THE M$ Realm and it is weird
            # We manage the address
            street_key = 'streetAddress'
            contact_obj[street_key] = vals['street'] + "\r\n" + vals['street2']
            # we modifiy the class
            contact_obj['objectclass'] = [
                'top',
                'person',
                'organizationalPerson',
                'inetOrgPerson',
                'user',
            ]
            # we handle the country
            if vals.get('country_id'):
                country = self.browse(cr, uid, id, context=context).country_id
                if country:
                    vals['country_id'] = country.name
                    vals['c'] = country.code
                else:
                    vals['country_id'] = False
                    vals['c'] = False
            if vals.get('country_id', False):
                self.getVals(
                    'co', 'country_id', vals, contact_obj, uid, id, cr,
                    context
                )
                self.getVals('c', 'c', vals, contact_obj, uid, id, cr, context)
            # we compute the display name
            vals['display'] = '%s %s' % (vals['partner'], contact_obj['cn'][0])
            # we get the title
            if self.browse(cr, uid, id).function:
                contact_obj['description'] = self.browse(
                    cr, uid, id).function.name
            # we replace carriage return
            if vals.get('comment', False):
                vals['comment'] = vals['comment'].replace("\n", "\r\n")
            # Active directory specific fields
            self.getVals(
                'company', 'partner', vals, contact_obj, uid, id, cr, context
            )
            self.getVals(
                'info', 'comment', vals, contact_obj, uid, id, cr, context
            )
            self.getVals(
                'displayName', 'partner', vals, contact_obj, uid, id, cr,
                context
            )
            # Web site management
            if self.browse(cr, uid, id).partner_id.website:
                vals['website'] = self.browse(cr, uid, id).partner_id.website
                self.getVals(
                    'wWWHomePage', 'website', vals, contact_obj, uid, id, cr,
                    context
                )
                del(vals['website'])
            self.getVals(
                'title', 'title', vals, contact_obj, uid, id, cr, context
            )
        else:
            contact_obj[street_key] = vals['street'] + u"\n" + vals['street2']
            self.getVals(
                'o', 'partner', vals, contact_obj, uid, id, cr, context
            )

        # Common attributes
        self.getVals(
            'givenName', 'firstname', vals, contact_obj, uid, id, cr, context
        )
        self.getVals('mail', 'email', vals, contact_obj, uid, id, cr, context)
        self.getVals(
            'telephoneNumber', 'phone', vals, contact_obj, uid, id, cr, context
        )
        self.getVals('l', 'city', vals, contact_obj, uid, id, cr, context)
        self.getVals(
            'facsimileTelephoneNumber', 'fax', vals, contact_obj, uid, id, cr,
            context
        )
        self.getVals(
            'mobile', 'mobile', vals, contact_obj, uid, id, cr, context
        )
        self.getVals(
            'homePhone', 'private_phone', vals, contact_obj, uid, id, cr,
            context
        )
        self.getVals(
            'postalCode', 'zip', vals, contact_obj, uid, id, cr, context
        )
        self.unUnicodize(contact_obj)
        return contact_obj

    def saveLdapContact(self, id, vals, cursor, uid, context=None):
        """save openerp adress to ldap"""
        contact_obj = self.mappLdapObject(id, vals, cursor, uid, context)
        conn = self.connectToLdap(cursor, uid, context=context)
        try:
            if self.getconn(cursor, uid, context).ACTIVDIR:
                conn.connexion.add_s(
                    "CN=%s,OU=%s,%s" % (contact_obj['cn'][0],
                                        conn.OU,
                                        conn.CONTACT_DN),
                    ldap.modlist.addModlist(contact_obj)
                )
            else:
                conn.connexion.add_s(
                    "uid=terp_%s,OU=%s,%s" % (str(id),
                                              conn.OU,
                                              conn.CONTACT_DN),
                    ldap.modlist.addModlist(contact_obj))
        except Exception:
            raise
        conn.connexion.unbind_s()

    def updateLdapContact(self, id, vals, cursor, uid, context):
        """update an existing contact with the data of OpenERP"""
        conn = self.connectToLdap(cursor, uid, context={})
        try:
            old_contatc_obj = self.getLdapContact(conn, id)
        except ldap.NO_SUCH_OBJECT:
            self.saveLdapContact(id, vals, cursor, uid, context)
            return
        contact_obj = self.mappLdapObject(id, vals, cursor, uid, context)
        if conn.ACTIVDIR:
            modlist = []
            for key, val in contact_obj.items():
                if key in ('cn', 'uid', 'objectclass'):
                    continue
                if isinstance(val, list):
                    val = val[0]
                modlist.append((ldap.MOD_REPLACE, key, val))
        else:
            modlist = ldap.modlist.modifyModlist(
                old_contatc_obj[1],
                contact_obj
            )
        try:
            conn.connexion.modify_s(old_contatc_obj[0], modlist)
            conn.connexion.unbind_s()
        except Exception:
            raise

    def removeLdapContact(self, id, cursor, uid):
        """Remove a contact from ldap"""
        conn = self.connectToLdap(cursor, uid, context={})
        to_delete = None
        try:
            to_delete = self.getLdapContact(conn, id)
        except ldap.NO_SUCH_OBJECT:
            logger.notifyChannel("Warning", netsvc.LOG_INFO,
                                 _("'no object to delete in ldap' %s") % (id))
        except Exception:
            raise
        try:
            if to_delete:
                conn.connexion.delete_s(to_delete[0])
                conn.connexion.unbind_s()
        except Exception:
            raise

    def getLdapContact(self, conn, id):
        result = conn.connexion.search_ext_s(
            "ou=%s, %s" % (conn.OU, conn.CONTACT_DN),
            ldap.SCOPE_SUBTREE,
            "(&(objectclass=*)(uid=terp_" + str(id) + "))"
        )
        if not result:
            raise ldap.NO_SUCH_OBJECT
        return result[0]

    def ldaplinkactive(self, cursor, uid, context=None):
        """Check if ldap is activated for this company"""
        users_pool = self.pool['res.users']
        user = users_pool.browse(cursor, uid, uid, context=context)
        return user.company_id.ldap_active

    def getconn(self, cursor, uid, context=None):
        """LdapConnMApper"""
        if not self.ldapMapper:
            self.ldapMapper = LdapConnMApper(cursor, uid, self)
        return self.ldapMapper

    def connectToLdap(self, cursor, uid, context=None):
        """Reinitialize ldap connection"""
        # getting ldap pref
        if not self.ldapMapper:
            self.getconn(cursor, uid, context)
        self.ldapMapper.get_connexion()
        return self.ldapMapper
