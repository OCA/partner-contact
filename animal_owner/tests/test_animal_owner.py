from odoo.tests.common import TransactionCase


class TestAnimalOwner(TransactionCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.test_species = self.env["animal.species"].create({"name": "specie 1"})
        self.test_breed = self.env["animal.breed"].create(
            {"name": "breed 1", "species_id": self.test_species.id}
        )
        self.test_animal = self.env["animal"].create(
            {
                "name": "Animal 1",
                "species_id": self.test_species.id,
                "breed_id": self.test_breed.id,
            }
        )
        self.test_partner = self.env["res.partner"].create({"name": "Test Partner"})

    def test_compute_animal_count(self):
        # Test partner when no animal
        self.assertEqual(self.test_partner.animal_count, 0)

        # Add an animal
        self.test_partner.write({"animal_ids": [(4, self.test_animal.id)]})
        self.assertEqual(self.test_partner.animal_count, 1)

        # Add another animal
        new_animal = self.env["animal"].create(
            {
                "name": "Animal 2",
                "species_id": self.test_species.id,
                "breed_id": self.test_breed.id,
            }
        )
        self.test_partner.write({"animal_ids": [(4, new_animal.id)]})
        self.assertEqual(self.test_partner.animal_count, 2)

        # Remove an animal
        self.test_partner.write({"animal_ids": [(3, self.test_animal.id)]})
        self.assertEqual(self.test_partner.animal_count, 1)

    def test_action_view_animals(self):
        # Remove all animals
        self.test_partner.animal_ids = []

        # Test action view animals when no animals
        action = self.test_partner.action_view_animals()
        self.assertEqual(action["res_id"], False)

        # Add an animal
        self.test_partner.write({"animal_ids": [(4, self.test_animal.id)]})
        action = self.test_partner.action_view_animals()
        self.assertEqual(action["res_id"], self.test_animal.id)

        # Add another animal
        new_animal = self.env["animal"].create(
            {
                "name": "Animal 2",
                "species_id": self.test_species.id,
                "breed_id": self.test_breed.id,
                "partner_id": self.test_partner.id,
            }
        )
        action = self.test_partner.action_view_animals()
        self.assertIn(new_animal.id, action["domain"][0][2])
