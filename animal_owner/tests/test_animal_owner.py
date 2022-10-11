# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.animal.tests import test_animal


class TestAnimalOwner(test_animal.TestAnimalState):
    def setUp(self):
        super(TestAnimalOwner, self).setUp()
        self.partner_obj = self.env["res.partner"]

        # Create Owner 1
        self.owner_1 = self.partner_obj.create({"name": "Owner 1"})
        self.owner_2 = self.partner_obj.create({"name": "Owner 2"})

        # Assign to test_animal
        self.test_animal.write({"partner_id": self.owner_1.id})

        # Duplicate test_animals for owner_2
        self.test_animal_1 = self.test_animal.copy()
        self.test_animal_1.write({"partner_id": self.owner_2.id})
        self.test_animal_2 = self.test_animal_1.copy()

    def test_animal_owner_1(self):
        # Test action 1
        self.owner_1.action_view_animals()

        # Check for animal count
        self.assertEqual(self.owner_1.animal_count, 1)

    def test_animal_owner_2(self):
        # Test action 2
        self.owner_2.action_view_animals()

        # Check for animal count
        self.assertEqual(self.owner_2.animal_count, 2)

        # Unlink animal
        self.owner_2.animal_ids.unlink()

        # Check animal count after unlink
        self.assertEqual(self.owner_2.animal_count, 0)
