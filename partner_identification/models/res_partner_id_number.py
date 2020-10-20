# -*- coding: utf-8 -*-
# Copyright - 2004-2010 Tiny SPRL http://tiny.be
# Copyright - 2010-2012 ChriCar Beteiligungs- und Beratungs- GmbH
#             http://www.camptocamp.at
# Copyright - 2015 Antiun Ingenieria, SL (Madrid, Spain)
#        http://www.antiun.com
#        Antonio Espinosa <antonioea@antiun.com>
# Copyright - 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=invalid-name,missing-docstring,too-many-arguments
# pylint: disable=protected-access,unused-argument,no-self-use
from openerp.osv import orm, fields


class ResPartnerIdNumber(orm.Model):
    _name = 'res.partner.id_number'
    _order = 'name'

    _columns = {
        'name': fields.char(
            "ID Number", required=True,
            help="The ID itself. For example, Driver License number of this "
                 "person"),
        'category_id': fields.many2one(
            'res.partner.id_category',
            "Category", required=True,
            help="ID type defined in configuration."
                 "For example, Driver License"),
        'partner_id': fields.many2one(
            'res.partner',
            "Partner", required=True,
            ondelete='cascade'),
        'partner_issued_id': fields.many2one(
            'res.partner',
            "Issued by",
            help="Another partner, who issued this ID. For example, Traffic "
                 "National Institution"),
        'place_issuance': fields.char(
            "Place of Issuance",
            help="The place where the ID has been issued. For example"
                 " the country for passports and visa"),
        'date_issued': fields.date(
            "Issued on",
            help="Issued date. For example, date when person approved"
                 " his driving exam, 21/10/2009"),
        'valid_from': fields.date(
            "Valid from",
            help="Validation period stating date."),
        'valid_until': fields.date(
            "Valid until",
            help="Expiration date. For example, date when person needs"
                 " to renew his driver license, 21/10/2019"),
        'comment': fields.text("Notes"),
        # TODO: rename status field to standard state.
        'status': fields.selection(
            [('draft', 'New'),
             ('open', 'Running'),
             ('pending', 'To Renew'),
             ('close', 'Expired')],
            "Status"),
        'active': fields.boolean(string="Active"),
    }
    _defaults = {
        'active': True,
    }

    def _validate_id_number(self, cr, uid, ids, context=None):
        category_model = self.pool['res.partner.id_category']
        for this in self.browse(cr, uid, ids, context=context):
            # Validation will throw exception when number invalid.
            category_model.validate_id_number(this, context=context)
        return True

    _constraints = [
        (_validate_id_number,
         'ID number is nots valid for this category.',
         ['name', 'category_id'])]
