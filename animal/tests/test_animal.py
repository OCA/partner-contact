from odoo.tests.common import TransactionCase


# @tagged('-at_install', 'post_install')
class TestAnimalState(TransactionCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)
        cls.test_species = cls.env["animal.species"].create({"name": "specie 1"})
        cls.test_breed = cls.env["animal.breed"].create(
            {"name": "breed 1", "species_id": cls.test_species.id}
        )
        cls.test_animal = cls.env["animal"].create(
            {
                "name": "Animal 1",
                "species_id": cls.test_species.id,
                "breed_id": cls.test_breed.id,
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
