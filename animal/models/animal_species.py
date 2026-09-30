# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class AnimalSpecies(models.Model):
    _name = "animal.species"
    _description = "Animal Species"
    _order = "name"

    name = fields.Char(translate=True)
    breed_ids = fields.One2many("animal.breed", "species_id", string="Breeds")
