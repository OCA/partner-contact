# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from lxml import etree

from openerp.osv import expression, fields
from openerp.osv.orm import transfer_modifiers_to_node
from openerp.tools.translate import _


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

    def make_field(self):
        return fields.one2many(
            'res.partner.relation',
            '%s_partner_id' % self.side,
            string=self.name,
            domain=self.get_domain())

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
        _logger.debug(
            _("Created page for %s tab %s with arch: %s"),
            self.side, self.name, etree.tostring(tab_page))
        return tab_page

    def _get_other_partner_domain(self):
        partner_domain = []
        if self.other_contact_type == 'c':
            partner_domain.append(('is_company', '=', True))
        if self.other_contact_type == 'p':
            partner_domain.append(('is_company', '=', False))
        if self.other_category_id:
            partner_domain.append(
                ('category_id', 'child_of', self.other_category_id.id))
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
                [('category_id', '!=', self.category_id.id)]])
        attrs = {'invisible': invisible}
        tab_page.set('attrs', repr(attrs))
        transfer_modifiers_to_node(attrs, tab_page)
