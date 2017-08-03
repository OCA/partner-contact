# -*- coding: utf-8 -*-
# © 2014-2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from lxml import etree
from odoo.osv.orm import Model, transfer_modifiers_to_node
from odoo.osv import expression
from odoo import api, _

TAB_LEFT = 'left'
TAB_RIGHT = 'right'


class ResPartner(Model):
    _inherit = 'res.partner'

    def _create_relation_type_tab(self, rel_type, current_tab_postfix,
                                  field_names):
        """Create an xml node containing the relation's tab to be added to the
        view. Add the field(s) created on the form to field_names."""
        name = rel_type.name if current_tab_postfix == TAB_LEFT \
            else rel_type.name_inverse
        contact_type = rel_type['contact_type_' + current_tab_postfix]
        partner_category = rel_type['partner_category_' + current_tab_postfix]
        tab = etree.Element('page')
        tab.set('string', name)
        invisible = [('id', '=', False)]
        if contact_type:
            invisible = expression.OR([
                invisible,
                [('is_company', '=', contact_type != 'c')]])
        if partner_category:
            invisible = expression.OR([
                invisible,
                [('category_id', '!=', partner_category.id)]])
        attrs = {
            'invisible': invisible,
        }
        tab.set('attrs', repr(attrs))
        transfer_modifiers_to_node(attrs, tab)
        field_name = 'relation_ids_own_tab_%s_%s' % (
            rel_type.id, current_tab_postfix)
        field_names.append(field_name)
        this_partner_name = '%s_partner_id' % (current_tab_postfix)
        other_partner_name = '%s_partner_id' % (
            TAB_RIGHT if current_tab_postfix == TAB_LEFT else TAB_LEFT)
        field = etree.Element(
            'field',
            name=field_name,
            context=('{"default_type_id": %s, "default_%s": id, '
                     '"active_test": False}') % (
                rel_type.id,
                this_partner_name))
        tab.append(field)
        tree = etree.Element('tree', editable='bottom')
        field.append(tree)
        partner_type = rel_type.contact_type_left \
            if current_tab_postfix == TAB_LEFT else rel_type.contact_type_right
        if partner_type == 'c':
            is_company = True
        else:
            is_company = False
        tree.append(etree.Element(
            'field',
            string=_('Partner'),
            domain=repr([('is_company', '=', is_company)]),
            name=other_partner_name))
        tree.append(etree.Element(
            'field',
            name='date_start'))
        tree.append(etree.Element(
            'field',
            name='date_end'))
        tree.append(etree.Element('field', name='type_id',
                                  invisible='True'))
        tree.append(etree.Element('field', name=this_partner_name,
                                  invisible='True'))
        return tab

    def _add_relation_type_tab(self, rel_type, field_names,
                               element_last_page_hook):
        """
        Adds the relevant tabs to the partner's formview.
        """
        if rel_type.own_tab_left:
            tab = self._create_relation_type_tab(
                rel_type, TAB_LEFT, field_names)
            element_last_page_hook.addnext(tab)
        if rel_type.own_tab_right and not rel_type.is_symmetric:
            tab = self._create_relation_type_tab(
                rel_type, TAB_RIGHT, field_names)
            element_last_page_hook.addnext(tab)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        result = super(ResPartner, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if view_type == 'form' and not self.env.context.get('check_view_ids'):
            res_partner_relation_type = self.env['res.partner.relation.type']
            own_tab_types = res_partner_relation_type.search(
                ['|',
                 ('own_tab_left', '=', True),
                 ('own_tab_right', '=', True)
                 ])
            view = etree.fromstring(result['arch'])
            element_last_page_hook = view.xpath('//page[last()]')
            element_last_page_hook = element_last_page_hook[0]
            field_names = []
            if not view.xpath('//field[@name="id"]'):
                view.append(etree.Element('field', name='id',
                                          invisible='True'))
                field_names.append('id')
            for rel_type in own_tab_types:
                self._add_relation_type_tab(
                    rel_type, field_names, element_last_page_hook)
            ir_ui_view_obj = self.env['ir.ui.view']
            result['arch'], fields = ir_ui_view_obj.postprocess_and_fields(
                self._name, view, result['view_id'])
            for field_name in field_names:
                result['fields'][field_name] = fields[field_name]
        return result
