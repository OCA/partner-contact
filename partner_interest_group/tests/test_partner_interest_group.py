# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestPartnerInterestGroup(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.InterestGroup = cls.env["res.partner.interest.group"]
        cls.Partner = cls.env["res.partner"]
        cls.group = cls.InterestGroup.create({"name": "Events"})
        cls.partner = cls.Partner.create({"name": "Test Partner"})

    def test_default_company(self):
        """A new interest group defaults to the current company."""
        self.assertEqual(self.group.company_id, self.env.company)

    def test_active_default(self):
        """Interest groups are active by default and support archiving."""
        self.assertTrue(self.group.active)
        self.group.action_archive()
        self.assertFalse(self.group.active)
        self.group.action_unarchive()
        self.assertTrue(self.group.active)

    def test_partner_interest_group_link(self):
        """Interest groups can be assigned to partners (both directions)."""
        self.partner.interest_group_ids = self.group
        self.assertIn(self.group, self.partner.interest_group_ids)
        self.assertIn(self.partner, self.group.partner_id)

    def test_archived_group_hidden_by_default(self):
        """Archived groups are excluded from a default search."""
        self.group.action_archive()
        self.assertNotIn(self.group, self.InterestGroup.search([]))
        self.assertIn(
            self.group,
            self.InterestGroup.search([("active", "=", False)]),
        )
