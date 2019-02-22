# -*- coding: utf-8 -*-
# Copyright - 2004-2010 Tiny SPRL http://tiny.be
# Copyright - 2010-2012 ChriCar Beteiligungs- und Beratungs- GmbH
#             http://www.camptocamp.at
# Copyright - 2015 Antiun Ingenieria, SL (Madrid, Spain)
#        http://www.antiun.com
#        Antonio Espinosa <antonioea@antiun.com>
# Copyright - 2016 ACSONE SA/NV (<http://acsone.eu>)
# Copyright - 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=invalid-name,missing-docstring,too-many-arguments
# pylint: disable=protected-access,unused-argument,no-self-use
from openerp.osv import orm, fields
from openerp.exceptions import Warning as UserError
from openerp.tools.safe_eval import safe_eval
from openerp.tools.translate import _


class ResPartnerIdCategory(orm.Model):
    _name = "res.partner.id_category"
    _order = "name"

    def default_get(self, cr, uid, fields, context=None):
        # pylint: disable=redefined-outer-name
        context = context or {}
        result = super(ResPartnerIdCategory, self).default_get(
            cr, uid, fields, context=context)
        if not fields or 'validation_code' in fields:
            result['validation_code'] = self._default_validation_code()
        if not fields or 'active' in fields:
            result['active'] = True
        return result

    def _default_validation_code(self):
        return _("\n# Python code. Use failed = True to specify that the id "
                 "number is not valid.\n"
                 "# You can use the following variables :\n"
                 "#  - self: browse_record of the current ID Category "
                 "browse_record\n"
                 "#  - id_number: browse_record of ID number to validate")

    _columns = {
        'code': fields.char(
            "Code", size=16, required=True,
            help="Abbreviation or acronym of this ID type. For example, "
                 "'driver_license'"),
        'name': fields.char(
            "ID name", required=True, translate=True,
            help="Name of this ID type. For example, 'Driver License'"),
        'active': fields.boolean(string="Active"),
        'validation_code': fields.text(
            'Python validation code',
            help="Python code called to validate an id number."),
    }

    def _validation_eval_context(self, id_number):
        return {
            'self': id_number.category_id,
            'id_number': id_number}

    def validate_id_number(self, id_number, context=None):
        """Validate the given ID number.

        The method raises an openerp.exceptions.ValidationError if the eval of
        python validation code fails.
        """
        context = context or {}
        if context.get('id_no_validate'):
            return
        eval_context = self._validation_eval_context(id_number)
        category = id_number.category_id
        try:
            safe_eval(
                category.validation_code, eval_context, mode='exec',
                nocopy=True)
        except Exception as e:
            raise UserError(
                _('Error when evaluating the id_category validation code:'
                  ':\n %s \n(%s)') % (category.name, e))
        if eval_context.get('failed', False):
            raise orm.except_orm(
                _('Error'),
                _("%s is not a valid %s identifier") % (
                    id_number.name, category.name))
