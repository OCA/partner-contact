# Copyright 2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from . import common

from ..tablib import Tab


class TestTab(common.TestCommon):

    def test_create_page(self):
        self.assertTrue(bool(self.tab_board))
        tab_obj = Tab(self.tab_board)
        page = tab_obj.create_page()
        # And we should have a field for (amongst others) selection_type_id.
        field = page.xpath('//field[@name="type_selection_id"]')
        self.assertTrue(field, 'Field selection_type_id not in page.')

    def test_visibility(self):
        """Tab positions should be shown for functionaries, but not others."""
        self.assertTrue(bool(self.tab_positions))
        self.assertTrue(bool(self.partner_important_person))
        self.assertTrue(bool(self.partner_common_person))
        tab_obj = Tab(self.tab_positions)
        self.assertTrue(
            tab_obj.compute_visibility(self.partner_important_person),
            'Positions tab should be visible for functionary.')
        self.assertFalse(
            tab_obj.compute_visibility(self.partner_common_person),
            'Positions tab should not be visible for non-functionary.')
        # Tab for departments should only be visible for main partner
        self.assertTrue(bool(self.tab_departments))
        self.assertTrue(bool(self.partner_big_company))
        tab_obj = Tab(self.tab_departments)
        self.assertTrue(
            tab_obj.compute_visibility(self.env.ref('base.main_partner')),
            'Department tab should be visible for main partner.')
        self.assertFalse(
            tab_obj.compute_visibility(self.partner_big_company),
            'Department tab should not be visible for other partners.')
