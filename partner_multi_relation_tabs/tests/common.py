# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestCommon(common.SingleTransactionCase):
    # pylint: disable=too-many-instance-attributes
    post_install = True

    def setUp(self):
        """Create common objects for tab tests."""
        # pylint: disable=invalid-name
        super(TestCommon, self).setUp()
        self.tab_model = self.env['res.partner.tab']
        self.type_model = self.env['res.partner.relation.type']
        self.partner_model = self.env['res.partner']
        self.relation_model = self.env['res.partner.relation']
        # Categories.
        self.category_government = self.env.ref(
            'partner_multi_relation_tabs.category_government')
        self.category_functionary = self.env.ref(
            'partner_multi_relation_tabs.category_functionary')
        self.category_department = self.env.ref(
            'partner_multi_relation_tabs.category_department')
        # Tabs.
        self.tab_committee = self.env.ref(
            'partner_multi_relation_tabs.tab_committee')
        self.tab_board = self.env.ref(
            'partner_multi_relation_tabs.tab_board')
        self.tab_positions = self.env.ref(
            'partner_multi_relation_tabs.tab_positions')
        self.tab_departments = self.env.ref(
            'partner_multi_relation_tabs.tab_departments')
        # Types.
        self.type_chairperson = self.env.ref(
            'partner_multi_relation_tabs'
            '.relation_type_committee_has_chairperson')
        self.type_ceo = self.env.ref(
            'partner_multi_relation_tabs'
            '.relation_type_company_has_ceo')
        # Partners.
        self.partner_big_company = self.env.ref(
            'partner_multi_relation_tabs.partner_big_company')
        self.partner_important_person = self.env.ref(
            'partner_multi_relation_tabs.partner_important_person')
        self.partner_common_person = self.env.ref(
            'partner_multi_relation_tabs.partner_common_person')
        # Relations.
        self.relation_company_ceo = self.env.ref(
            'partner_multi_relation_tabs.relation_company_ceo')
