# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from . import common


class TestResPartnerRelationType(common.TestCommon):

    def test_get_tabs(self):
        cr, uid = self.cr, self.uid
        self.assertTrue(bool(self.type_has_chairperson))
        # We should find the tab in get_tabs
        tabs = self.type_model.get_tabs(cr, uid)
        self.assertTrue(
            self.type_has_chairperson.id in [tab.id for tab in tabs])
