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
                "groups_id": [
                    (4, cls.env.ref("base.group_partner_manager").id),
                    (4, cls.env.ref("base.group_user").id),
                ],
            }
        )

    def test_contact_creation_access(self):
        with self.assertRaises(AccessError):
            self.env["res.partner"].with_user(self.user).create({"name": "New Partner"})

        self.user.can_create_contacts = True
        partner = (
            self.env["res.partner"].with_user(self.user).create({"name": "New Partner"})
        )
        self.assertTrue(partner.id, "Partner should be created")

    def test_system_user_access(self):
        system_user = self.env["res.users"].create(
            {
                "name": "System User",
                "login": "systemuser",
                "can_create_contacts": False,
                "groups_id": [
                    (4, self.env.ref("base.group_system").id),
                    (4, self.env.ref("base.group_user").id),
                    (4, self.env.ref("base.group_partner_manager").id),
                ],
            }
        )
        partner = (
            self.env["res.partner"]
            .with_user(system_user)
            .create({"name": "System User Partner"})
        )
        self.assertTrue(partner.id, "Partner should be created by system user")

    def test_superuser_access(self):
        self.env.user.can_create_contacts = False
        partner = self.env["res.partner"].create({"name": "Superuser Partner"})
        self.assertTrue(partner.id, "Partner should be created by superuser")
