from odoo.tests.common import TransactionCase


# @tagged('-at_install', 'post_install')
class TestAnimalState(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestAnimalState, self).setUp(*args, **kwargs)
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

    def test_onchange_species(self):
        self.test_animal.onchange_species()
        self.assertEqual(
            self.test_animal.breed_id.id,
            False,
            "Animal breed_id should be changed to False",
        )

    def test_onchange_breed(self):
        self.test_animal.onchange_breed()
        self.assertEqual(
            self.test_animal.color_id.id,
            False,
            "Animal color_id should be changed to False",
        )
