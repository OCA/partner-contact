# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from lxml import etree

from openerp.osv import orm


class ResPartner(orm.Model):
    _inherit = 'res.partner'

    def browse(
            self, cr, uid, select, context=None, list_class=None,
            fields_process=None):
        for tab in self._get_tabs(cr, uid, context=context):
            fieldname = tab.get_fieldname()
            if fieldname not in self._columns:
                # Check this for performance reasons.
                self._columns[fieldname] = tab.make_field()
        return super(ResPartner, self).browse(
            cr, uid, select, context=context, list_class=list_class,
            fields_process=fields_process)

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
        extra_fields = self._add_tab_pages(cr, uid, view, context=context)
        result['arch'], view_fields = self._BaseModel__view_look_dom_arch(
            cr, uid, view, result['view_id'], context=context)
        for fieldname in extra_fields:
            result['fields'][fieldname] = view_fields[fieldname]
        return result

    def _add_tab_pages(self, cr, uid, view, context=None):
        """Adds the relevant tabs to the partner's formview.

        This should only be done for those partner forms that have
        pages in the first place. Some specialized forms contain only
        a limited selection of fiels and no pages/tabs.
        """
        last_page_nodes = view.xpath('//page[last()]')
        if not last_page_nodes:
            return []
        extra_fields = []
        if not view.xpath('//field[@name="id"]'):
            view.append(
                etree.Element('field', name='id', invisible='True'))
            extra_fields.append('id')
        last_page = last_page_nodes[0]
        for tab in self._get_tabs(cr, uid, context=context):
            fieldname = tab.get_fieldname()
            self._columns[fieldname] = tab.make_field()
            extra_fields.append(fieldname)
            tab_page = tab.create_page()
            last_page.addnext(tab_page)
            last_page = tab_page  # Keep ordering of tabs
        return extra_fields

    def _get_tabs(self, cr, uid, context=None):
        relation_type_model = self.pool['res.partner.relation.type']
        return relation_type_model.get_tabs(cr, uid, context=context)

    def _get_relation_ids_select_from(self, field_name=None):
        base_from = super(ResPartner, self)\
            ._get_relation_ids_select_from(field_name=field_name)
        from_extend = \
            "JOIN res_partner_relation_type rprt ON rpr.type_id = rprt.id"
        return "%s %s" % (base_from, from_extend)

    def _get_relation_ids_select_where(self, field_name=None):
        # Need to completely override the super method!
        return (
            "WHERE ((rpr.left_partner_id in %s AND rprt.own_tab_left=False)"
            " OR (rpr.right_partner_id in %s AND rprt.own_tab_right=False))")
