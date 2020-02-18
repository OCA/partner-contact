# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from lxml import etree

from . import common


class TestResPartner(common.TestCommon):

    def test_fields_view_get(self):
        self.assertTrue(bool(self.type_has_chairperson))
        # The form view for partner should contain id:
        field = self._get_partner_view_field('form', 'id')
        self.assertTrue(field, 'Id field not in form.')
        # And we should have a field for the tab:
        fieldname = self.chairperson_tab.get_fieldname()
        field = self._get_partner_view_field('form', fieldname)
        self.assertTrue(field, 'Field %s not in form.' % fieldname)
        # There should be no effect on the tree view:
        field = self._get_partner_view_field('tree', fieldname)
        self.assertFalse(field, 'Field %s should not be in tree.' % fieldname)

    def _get_partner_view_field(self, view_type, fieldname):
        cr, uid = self.cr, self.uid
        view = self.partner_model.fields_view_get(cr, uid, view_type=view_type)
        tree = etree.fromstring(view['arch'])
        field = tree.xpath('//field[@name="%s"]' % fieldname)
        return field
