# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class AnimalBreed(models.Model):
    _name = "animal.breed"
    _description = "Animal Breeds"
    _order = "name"

    name = fields.Char(translate=True)
    species_id = fields.Many2one("animal.species", string="Species", required=True)
