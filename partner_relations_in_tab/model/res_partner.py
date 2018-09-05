# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from lxml import etree

from openerp.osv import orm, fields
from openerp.tools.translate import _

from ..tablib import Tab


_logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ResPartner(orm.Model):
    _inherit = 'res.partner'

    def _register_hook(self, cr):
        """This function is automatically called by Odoo on all models."""
        self._update_tab_fields(cr)

    def _update_tab_fields(self, cr):
        """Create a field for each tab that might be shown for a partner."""
        deprecated_tab_fields = [
            name for name in self._columns.copy()
            if Tab.is_tab_fieldname(name)]
        tabs = self._get_tabs(cr)
        for tab in tabs:
            fieldname = self._add_tab_field(tab)
            if fieldname in deprecated_tab_fields:
                deprecated_tab_fields.remove(fieldname)  # not deprecated
        for fieldname in deprecated_tab_fields:
            self._delete_tab_field(fieldname)

    def _get_tabs(self, cr):
        relation_type_model = self.pool['res.partner.relation.type']
        return relation_type_model.get_tabs(cr)

    def _add_tab_field(self, tab):
        fieldname = tab.get_fieldname()
        field = fields.one2many(
            'res.partner.relation',
            '%s_partner_id' % tab.side,
            string=tab.name,
            domain=tab.get_domain())
        if fieldname in self._columns:
            _logger.info(_(
                "Updating field %s in res.partner model.") % fieldname)
        else:
            _logger.info(_(
                "Adding field %s to res.partner model.") % fieldname)
        self._columns[fieldname] = field
        return fieldname

    def _delete_tab_field(self, fieldname):
        _logger.info(_(
            "Deleting field %s from res.partner model.") % fieldname)
        del self._columns[fieldname]

    def fields_view_get(
            self, cr, uid, view_id=None, view_type='form', context=None,
            toolbar=False, submenu=False):
        context = context or {}
        result = super(ResPartner, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar, submenu=submenu)
        if view_type != 'form' or context.get('check_view_ids'):
            return result
        view = etree.fromstring(result['arch'])
        extra_fields = self._add_tab_pages(cr, view)
        result['arch'], view_fields = self._BaseModel__view_look_dom_arch(
            cr, uid, view, result['view_id'], context=context)
        for fieldname in extra_fields:
            result['fields'][fieldname] = view_fields[fieldname]
        return result

    def _add_tab_pages(self, cr, view):
        """Adds the relevant tabs to the partner's formview."""
        extra_fields = []
        if not view.xpath('//field[@name="id"]'):
            view.append(
                etree.Element('field', name='id', invisible='True'))
            extra_fields.append('id')
        element_last_page_hook = view.xpath('//page[last()]')[0]
        for tab in self._get_tabs(cr):
            fieldname = tab.get_fieldname()
            extra_fields.append(fieldname)
            tab_page = tab.create_page()
            _logger.debug(
                _("Adding %s tab %s with arch: %s"),
                tab.side, tab.name, etree.tostring(tab_page))
            element_last_page_hook.addnext(tab_page)
        return extra_fields

    def _get_relation_ids_select(
            self, cr, uid, ids, fieldname, arg, context=None):
        """Overide domain for other partner on default relations tab."""
        cr.execute(
            """select r.id, left_partner_id, right_partner_id
            from res_partner_relation r
                join res_partner_relation_type t
                    on r.type_id = t.id
            where ((left_partner_id in %s and own_tab_left=False)
                or (right_partner_id in %s and own_tab_right=False))""" +
            ' order by ' + self.pool['res.partner.relation']._order,
            (tuple(ids), tuple(ids)))
        return cr.fetchall()
