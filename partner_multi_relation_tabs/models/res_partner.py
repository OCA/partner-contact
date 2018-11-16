# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from lxml import etree

from odoo.osv.orm import transfer_modifiers_to_node
from odoo.osv import expression
from odoo import _, api, fields, models


_logger = logging.getLogger(__name__)
NAME_PREFIX = 'relation_ids_tab'


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_tab_fieldname(self, tab):
        """Create fieldname for tab."""
        return '%s_%s' % (NAME_PREFIX, tab.id)

    @api.model
    def _add_tab_field(self, tab):
        fieldname = self._get_tab_fieldname(tab)
        _logger.info(_(
            "Adding field %s to res.partner model." % fieldname))
        field = fields.One2many(
            comodel_name='res.partner.relation.all',
            inverse_name='this_partner_id',
            domain=[('tab_id', '=', tab.id)],
            string=tab.name)
        self._add_field(fieldname, field)

    @api.model
    def _update_tab_field(self, tab):
        fieldname = self._get_tab_fieldname(tab)
        if fieldname not in self._fields:
            return self._add_tab_field(tab)
        _logger.info(_(
            "Updating field %s in res.partner model." % fieldname))
        self._fields[fieldname].string = tab.name

    @api.model
    def _delete_tab_field(self, fieldname):
        _logger.info(_(
            "deleting field %s from res.partner model." % fieldname))
        self._pop_field(fieldname)

    @api.model
    def _update_tab_fields(self):
        """Create a field for each tab that might be shown for a partner."""
        deprecated_tab_fields = [
            name for name in self._fields
            if name.startswith(NAME_PREFIX)]
        tab_model = self.env['res.partner.tab']
        for tab in tab_model.search([]):  # get all tabs
            fieldname = self._get_tab_fieldname(tab)
            self._add_tab_field(tab)
            if fieldname in deprecated_tab_fields:
                deprecated_tab_fields.remove(fieldname)  # not deprecated
        for fieldname in deprecated_tab_fields:
            self._delete_tab_field(fieldname)

    def _register_hook(self):
        self._update_tab_fields()

    def _create_tab_page(self, fieldname, tab):
        """Create an xml node containing the tab page to be added view."""
        # pylint: disable=no-member
        tab_page = etree.Element('page')
        invisible = [('id', '=', False)]  # Partner not created yet
        if tab.partner_ids:
            invisible = expression.OR([
                invisible,
                [('id', 'not in', tab.partner_ids.ids)]])
        else:
            if tab.contact_type:
                invisible = expression.OR([
                    invisible,
                    [('is_company', '=', tab.contact_type != 'c')]])
            if tab.partner_category_id:
                invisible = expression.OR([
                    invisible,
                    [('category_id', '!=', tab.partner_category_id.id)]])
        attrs = {'invisible': invisible}
        tab_page.set('string', tab.name)
        tab_page.set('attrs', repr(attrs))
        transfer_modifiers_to_node(attrs, tab_page)
        field = etree.Element(
            'field',
            name=fieldname,
            context='{'
                    '"default_this_partner_id": id,'
                    '"default_tab_id": %d,'
                    '"active_test": False}' % tab.id)
        tree = etree.Element('tree', editable='bottom')
        # Now add fields for the editable tree view in the tab:
        type_field = etree.Element(
            'field',
            name='type_selection_id',
            widget='many2one_clickable')
        type_field.set('domain', repr([('tab_id', '=', tab.id)]))
        type_field.set('options', repr({'no_create': True}))
        tree.append(type_field)
        other_partner_field = etree.Element(
            'field',
            name='other_partner_id',
            widget='many2one_clickable')
        other_partner_field.set('options', repr({'no_create': True}))
        tree.append(other_partner_field)
        tree.append(etree.Element('field', name='date_start'))
        tree.append(etree.Element('field', name='date_end'))
        field.append(tree)
        tab_page.append(field)
        return tab_page

    def _add_tab_pages(self, view):
        """Adds the relevant tabs to the partner's formview."""
        # pylint: disable=no-member
        last_page_nodes = view.xpath('//page[last()]')
        if not last_page_nodes:
            # Nothing to do if form contains no pages/tabs.
            return []
        extra_fields = []
        if not view.xpath('//field[@name="id"]'):
            view.append(
                etree.Element('field', name='id', invisible='True'))
            extra_fields.append('id')
        last_page = last_page_nodes[0]
        tab_model = self.env['res.partner.tab']
        for tab in tab_model.search([]):  # get all tabs
            fieldname = self._get_tab_fieldname(tab)
            self._update_tab_field(tab)
            extra_fields.append(fieldname)
            tab_page = self._create_tab_page(fieldname, tab)
            last_page.addnext(tab_page)
            last_page = tab_page  # Keep ordering of tabs
        return extra_fields

    @api.model
    def fields_view_get(
            self, view_id=None, view_type='form', toolbar=False,
            submenu=False):
        """Override to add relation tabs to form."""
        result = super(ResPartner, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if view_type != 'form' or self.env.context.get('check_view_ids'):
            return result
        view = etree.fromstring(result['arch'])  # pylint: disable=no-member
        extra_fields = self._add_tab_pages(view)
        view_model = self.env['ir.ui.view']
        result['arch'], original_fields = view_model.postprocess_and_fields(
            self._name, view, result['view_id'])
        for fieldname in extra_fields:
            result['fields'][fieldname] = original_fields[fieldname]
        return result
