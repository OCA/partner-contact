# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from lxml import etree

from openerp.osv.orm import Model, transfer_modifiers_to_node
from openerp.osv import expression, fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID


_logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
NAME_PREFIX = 'relation_ids_tab'


class Tab(object):

    def __init__(self, source, side):
        """Create tab from source.

        In this version source can be assumed to be a partner.relation.type.
        """
        self.id = source.id
        self.side = side
        if side == 'left':
            self.name = source.name
            self.contact_type = source.contact_type_left
            self.category_id = source.partner_category_left
            self.other_contact_type = source.contact_type_right
            self.other_category_id = source.partner_category_right
            self.other_side = 'right'
        else:
            self.name = source.name_inverse
            self.contact_type = source.contact_type_right
            self.category_id = source.partner_category_right
            self.other_contact_type = source.contact_type_left
            self.other_category_id = source.partner_category_left
            self.other_side = 'left'

    def get_fieldname(self):
        return '%s_%s_%s' % (NAME_PREFIX, self.id, self.side)

    def get_domain(self):
        return [('type_id', '=', self.id)]

    def create_page(self):
        tab_page = etree.Element('page')
        self._set_page_attrs(tab_page)
        field = etree.Element(
            'field',
            name=self.get_fieldname(),
            context=(
                '{"default_type_id": %s, "default_%s_partner_id": id, '
                '"active_test": False}') % (self.id, self.side))
        tab_page.append(field)
        tree = etree.Element('tree', editable='bottom')
        field.append(tree)
        tree.append(etree.Element(
            'field', name='%s_partner_id' % self.side, invisible='True'))
        tree.append(etree.Element(
            'field',
            string=_('Partner'),
            domain=repr(self._get_other_partner_domain()),
            widget='many2one_clickable',
            name='%s_partner_id' % self.other_side))
        tree.append(etree.Element('field', name='date_start'))
        tree.append(etree.Element('field', name='date_end'))
        tree.append(etree.Element('field', name='active'))
        tree.append(etree.Element('field', name='type_id', invisible='True'))
        return tab_page

    def _get_other_partner_domain(self):
        partner_domain = []
        if self.other_contact_type == 'c':
            partner_domain.append(('is_company', '=', True))
        if self.other_contact_type == 'p':
            partner_domain.append(('is_company', '=', False))
        if self.other_category_id:
            partner_domain.append(
                ('category_id', 'child_of', self.other_category_id))
        return partner_domain

    def _set_page_attrs(self, tab_page):
        tab_page.set('string', self.name)
        invisible = [('id', '=', False)]
        if self.contact_type:
            invisible = expression.OR([
                invisible,
                [('is_company', '=', self.contact_type != 'c')]])
        if self.category_id:
            invisible = expression.OR([
                invisible,
                [('category_id', '!=', self.category_id)]])
        attrs = {'invisible': invisible}
        tab_page.set('attrs', repr(attrs))
        transfer_modifiers_to_node(attrs, tab_page)


class ResPartner(Model):
    _inherit = 'res.partner'

    def _make_tab(self, source, side):
        return Tab(source, side)

    def _register_hook(self, cr):
        """This function is automatically called by Odoo on all models."""
        self._update_tab_fields(cr)

    def _update_tab_fields(self, cr):
        """Create a field for each tab that might be shown for a partner."""
        deprecated_tab_fields = [
            name for name in self._columns.copy()
            if name.startswith(NAME_PREFIX)]
        tabs = self._get_tabs(cr)
        for tab in tabs:
            fieldname = tab.get_fieldname()
            if fieldname in self._columns:
                self._update_tab_field(tab)
            else:
                self._add_tab_field(tab)
            if fieldname in deprecated_tab_fields:
                deprecated_tab_fields.remove(fieldname)  # not deprecated
        for fieldname in deprecated_tab_fields:
            self._delete_tab_field(fieldname)

    def _get_tabs(self, cr):
        tabs = []
        relation_type_model = self.pool['res.partner.relation.type']
        relation_type_domain = [
            '|',
            ('own_tab_left', '=', True),
            ('own_tab_right', '=', True)]
        relation_type_ids = relation_type_model.search(
            cr, SUPERUSER_ID, relation_type_domain)
        for relation_type in relation_type_model.browse(
                cr, SUPERUSER_ID, relation_type_ids):
            if relation_type.own_tab_left:
                new_tab = Tab(relation_type, 'left')
                tabs.append(new_tab)
            if relation_type.own_tab_right:
                new_tab = Tab(relation_type, 'right')
                tabs.append(new_tab)
        return tabs

    def _add_tab_field(self, tab):
        field = fields.one2many(
            'res.partner.relation',
            '%s_partner_id' % tab.side,
            string=tab.name,
            domain=tab.get_domain())
        fieldname = tab.get_fieldname()
        _logger.info(_(
            "Adding field %s to res.partner model.") % fieldname)
        self._columns[fieldname] = field

    def _update_tab_field(self, tab):
        fieldname = tab.get_fieldname()
        _logger.info(_(
            "Updating field %s in res.partner model.") % fieldname)
        self._columns[fieldname].string = tab.name

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
