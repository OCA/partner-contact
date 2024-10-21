from odoo.exceptions import ValidationError
from odoo.tests import common


class TestMaxDepth(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["ir.config_parameter"].set_param(
            "partner_contact_restrict_depth.contacts_max_depth", "0"
        )
        cls.parent_0 = cls.env["res.partner"].create(
            {"name": "Contact Parent 0", "parent_id": False}
        )

    def create_partner(self, name, parent_id=False):
        partner = self.env["res.partner"].create({"name": name, "parent_id": parent_id})
        return partner

    def test_no_max_depth(self):
        # Create child 1
        child1 = self.create_partner("Child-1", self.parent_0.id)

        self.assertEqual(self.parent_0.depth, 0)
        self.assertEqual(child1.depth, 1)
        self.assertEqual(child1.parent_id.id, self.parent_0.id)

        # Create child 1-1
        child1_1 = self.create_partner("Child-1.1", child1.id)

        self.assertEqual(child1_1.depth, 2)
        self.assertEqual(child1_1.parent_id.id, child1.id)

    def test_max_depth(self):
        # Max depth set to 1, so will be just allowed one level in the hierarchy of contacts
        self.env["ir.config_parameter"].set_param(
            "partner_contact_restrict_depth.contacts_max_depth", "1"
        )

        # Create child 1 (Will be allowed)
        child1 = self.create_partner("Child-1", self.parent_0.id)

        self.assertEqual(self.parent_0.depth, 0)
        self.assertEqual(child1.depth, 1)
        self.assertEqual(child1.parent_id.id, self.parent_0.id)

        # Create child 1-1 (Will be not allowed because would be depth 2 and maximum depth is 1)
        with self.assertRaises(ValidationError):
            self.create_partner("Child-1.1", child1.id)

    def test_depth_reparenting(self):
        self.env["ir.config_parameter"].set_param(
            "partner_contact_restrict_depth.contacts_max_depth", "2"
        )

        self.parent_1 = self.env["res.partner"].create(
            {"name": "Contact Parent 1", "parent_id": False}
        )

        child_01 = self.create_partner("Child-01", self.parent_0.id)
        child_11 = self.create_partner("Child-11", self.parent_1.id)

        self.assertEqual(self.parent_0.depth, 0)
        self.assertEqual(self.parent_1.depth, 0)
        self.assertEqual(child_01.depth, 1)
        self.assertEqual(child_11.depth, 1)
        self.assertEqual(child_01.parent_id.id, self.parent_0.id)
        self.assertEqual(child_11.parent_id.id, self.parent_1.id)

        child_11.write({"parent_id": child_01})
        self.assertEqual(child_11.depth, 2)
        self.assertEqual(child_11.parent_id.id, child_01.id)
        self.assertEqual(self.parent_0.depth, 0)
        self.assertEqual(child_01.depth, 1)
