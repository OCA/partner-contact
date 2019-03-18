# -*- coding: utf-8 -*-
# Copyright - 2004-2010 Tiny SPRL http://tiny.be
# Copyright - 2010-2012 ChriCar Beteiligungs- und Beratungs- GmbH
#             http://www.camptocamp.at
# Copyright - Antiun Ingenieria, SL (Madrid, Spain)
#        http://www.antiun.com
#        Antonio Espinosa <antonioea@antiun.com>
# Copyright - 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=invalid-name,missing-docstring,too-many-arguments
# pylint: disable=protected-access,unused-argument,no-self-use
from openerp.osv import orm, fields
from openerp.tools.translate import _
from openerp.osv.expression import is_leaf, AND


class ResPartner(orm.Model):
    """Base class to support identification fields.

    The base class provides for the registration of categories of
    identification and a list of those id numbers related to a partner.

    Inheriting modules can have specific fields, to enable easy entry and
    search on those fields. An example of souch a field follows here:

    Example:
        .. code-block:: python

        _columns = {
            'social_security': fields.function(
                lambda self, *args, **kwargs:
                self._compute_identification(*args, **kwargs),
                arg='SSN',
                fnct_inv=lambda self, *args, **kwargs:
                self._inverse_identification(*args, **kwargs),
                fnct_inv_arg='SSN',
                type='char',
                fnct_search=lambda self, *args, **kwargs:
                self._search_identification(*args, **kwargs),
                method=True, readonly=False,
                string='Social Security Number',
            ),
        }

    The field attributes arg and fnct_inv_arg must be set to a valid
    category code, to be provided by the module data of the module
    adding the field.
    """
    _inherit = 'res.partner'

    _columns = {
        'id_numbers': fields.one2many(
            'res.partner.id_number',
            'partner_id',
            "Identification Numbers"
        ),
    }

    def _compute_identification(
            self, cr, uid, ids, field_name, category_code, context=None):
        """ Compute the field that indicate a certain ID type.

        Use this on a field that represents a certain ID type. It will compute
        the desired field as that ID(s).

        This ID can be worked with as if it were a Char field, but it will
        be relating back to a ``res.partner.id_number`` instead.

        Args:
            field_name (str): Name of field to set.
            category_code (str): Category code of the Identification type.
        """
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = False
            if not record.id_numbers:
                continue
            for id_number in record.id_numbers:
                if id_number.category_id.code != category_code:
                    continue
                res[record.id] = id_number.name
        return res

    def _inverse_identification(
            self, cr, uid, ids, field_name, field_value, category_code,
            context=None):
        """ Inverse for an identification field.

        This method will create a new record, or modify the existing one
        in order to allow for the associated field to work like a Char.

        If a category does not exist of the correct code, it will be created
        using `category_code` as both the `name` and `code` values.

        If the value of the target field is unset, the associated ID will
        be deactivated in order to preserve history.

        Args:
            field_name (str): Name of field to set.
            category_code (str): Category code of the Identification type.
        """
        # For the moment do nothing with empty value.
        if not field_name or not field_value:
            return
        # Check, and if needed autocreate, category:
        category_id = self._get_create_category(
            cr, uid, category_code, context=context)
        id_model = self.pool['res.partner.id_number']
        for record in self.browse(cr, uid, ids, context=context):
            # Search all records with the right category.
            id_number_ids = id_model.search(
                cr, uid, [
                    ('partner_id', '=', record.id),
                    ('category_id', '=', category_id)],
                context=context)
            if len(id_number_ids) > 1:
                # Guard against writing wrong records.
                raise orm.except_orm(
                    _('Error'),
                    _('This %s has multiple IDs of this type (%s), so a write'
                      ' via the %s field is not possible.\n'
                      'In order to fix this, please use the IDs tab.') % (
                          record._name, category_code, field_name))
            if len(id_number_ids) < 1:
                id_model.create(
                    cr, uid, {
                        'partner_id': record.id,
                        'category_id': category_id,
                        'name': field_value},
                    context=context)
                return
            # There was an identification record singleton found.
            id_model.write(
                cr, uid, id_number_ids, {'name': field_value}, context=context)

    def _search_identification(
            self, cr, uid, dummy_obj, field_name, args, context=None):
        """ Search method for an identification field.

        Args:
            category_code (str): Category code of the Identification type.
            operator (str): Operator of domain.
            value (str): Value to search for.

        Returns:
            list: Domain to search with.
        """
        category_code = self._columns[field_name]._arg
        category_id = self._get_create_category(
            cr, uid, category_code, context=context)
        result = [('id_numbers.category_id.id', '=', category_id)]
        for arg in args:
            if is_leaf(arg) and arg[0] == field_name:
                result = AND([result, [('id_numbers.name', arg[1], arg[2])]])
        return result

    def _get_create_category(self, cr, uid, category_code, context=None):
        """Get category for code, create if not exists."""
        category_model = self.pool['res.partner.id_category']
        category_ids = category_model.search(
            cr, uid, [('code', '=', category_code)], context=context)
        if category_ids:
            return category_ids[0]
        category = category_model.create(
            cr, uid, {
                'code': category_code,
                'name': category_code},
            context=context)
        return category.id
