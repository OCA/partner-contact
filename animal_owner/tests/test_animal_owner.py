# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.animal.tests import test_animal


class TestAnimalOwner(test_animal.TestAnimalState):
    def setUp(self):
        super(TestAnimalOwner, self).setUp()
        self.partner_obj = self.env["res.partner"]

        # Create Partner
        self.partner = self.partner_obj.create({"name": "Partner 1"})

        # Assign to test_animal
        self.test_animal.write({
            "partner_id": self.partner.id
        })

    def test_animal_owner(self):
        # Test action
        self.partner.action_view_animals()

        # Check for animal count
        self.assertEqual(self.partner.animal_count, 1)

        # Unlink animal
        self.test_animal.unlink()

        # Check animal count after link
        self.assertEqual(self.partner.animal_count, 0)
