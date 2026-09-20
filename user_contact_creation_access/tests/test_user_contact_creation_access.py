from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestUserContactCreationAccess(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env["res.users"].create(
            {
                "name": "Test User Contact Creator",
                "login": "testusercontactcreator",
                "can_create_contacts": False,
            }
        )

    def test_contact_creation_access(self):
        with self.assertRaises(AccessError):
            self.env["res.partner"].with_user(self.user).create({"name": "New Partner"})

        self.user.can_create_contacts = True
        partner = (
            self.env["res.partner"].with_user(self.user).create({"name": "New Partner"})
        )
        self.assertEqual(partner.name, "New Partner")
