# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from lxml import etree
from openerp.osv.orm import Model, transfer_modifiers_to_node
from openerp.osv import expression
from openerp.tools.translate import _


class ResPartner(Model):
    _inherit = 'res.partner'

    def _get_relation_ids_select(self, cr, uid, ids, field_name, arg,
                                 context=None):
        cr.execute(
            '''select r.id, left_partner_id, right_partner_id
            from res_partner_relation r
                join res_partner_relation_type t
                    on r.type_id = t.id
            where ((left_partner_id in %s and own_tab_left=False)
                or (right_partner_id in %s and own_tab_right=False))''' +
            ' order by ' + self.pool['res.partner.relation']._order,
            (tuple(ids), tuple(ids))
        )
        return cr.fetchall()

    def _create_relation_type_tab(
            self, cr, uid, rel_type, inverse, field_names, context=None):
        '''Create an xml node containing the relation's tab to be added to the
        view. Add the field(s) created on the form to field_names.'''
        name = rel_type.name if not inverse else rel_type.name_inverse
        contact_type = rel_type['contact_type_' +
                                ('left' if not inverse else 'right')]
        partner_category = rel_type['partner_category_' +
                                    ('left' if not inverse
                                     else 'right')]
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
            rel_type.id,
            'left' if not inverse else 'right')
        field_names.append(field_name)
        this_partner_name = '%s_partner_id' % (
            'left' if not inverse else 'right')
        other_partner_name = '%s_partner_id' % (
            'left' if inverse else 'right')

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

        onchange_type_values = self.pool['res.partner.relation']\
            .on_change_type_selection_id(cr, uid, None,
                                         rel_type.id * 10 +
                                         (1 if inverse else 0),
                                         context=context)
        tree.append(etree.Element(
            'field',
            string=_('Partner'),
            domain=repr(
                onchange_type_values['domain']['partner_id_display']),
            widget='many2one_clickable',
            name=other_partner_name))
        tree.append(etree.Element(
            'field',
            name='date_start'))
        tree.append(etree.Element(
            'field',
            name='date_end'))
        tree.append(etree.Element(
            'field',
            name='active'))
        tree.append(etree.Element('field', name='type_id',
                                  invisible='True'))
        tree.append(etree.Element('field', name=this_partner_name,
                                  invisible='True'))
        return tab

    def _add_relation_type_tab(
            self, cr, uid, rel_type, inverse, field_names, relation_tab,
            context=None):
        '''add the xml node to the view'''
        tab = self._create_relation_type_tab(
            cr, uid, rel_type, inverse, field_names, context=context)
        relation_tab.addnext(tab)

    def fields_view_get(self, cr, uid, view_id=None, view_type='form',
                        context=None, toolbar=False, submenu=False):
        if context is None:
            context = {}
        result = super(ResPartner, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar, submenu=submenu)
        if view_type == 'form' and not context.get('check_view_ids'):
            res_partner_relation_type = self.pool['res.partner.relation.type']
            own_tab_types = res_partner_relation_type.browse(
                cr, uid,
                res_partner_relation_type.search(
                    cr, uid,
                    [
                        '|',
                        ('own_tab_left', '=', True),
                        ('own_tab_right', '=', True)
                    ],
                    context=context),
                context=context)
            view = etree.fromstring(result['arch'])

            relation_tab = view.xpath(
                '//field[@name="relation_ids"]/ancestor::page')
            if not relation_tab:
                return result
            relation_tab = relation_tab[0]

            field_names = []

            if not view.xpath('//field[@name="id"]'):
                view.append(etree.Element('field', name='id',
                                          invisible='True'))
                field_names.append('id')

            for rel_type in own_tab_types:
                if rel_type.own_tab_left:
                    self._add_relation_type_tab(
                        cr, uid, rel_type, False, field_names, relation_tab,
                        context=context)
                if rel_type.own_tab_right:
                    self._add_relation_type_tab(
                        cr, uid, rel_type, True, field_names, relation_tab,
                        context=context)

            result['arch'], fields = self\
                ._BaseModel__view_look_dom_arch(
                    cr, uid, view, result['view_id'], context=context)

            for field_name in field_names:
                result['fields'][field_name] = fields[field_name]

        return result
