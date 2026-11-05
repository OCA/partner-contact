# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class Animal(models.Model):
    _name = "animal"
    _description = "Animal"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char()
    ref = fields.Char(string="Reference")
    species_id = fields.Many2one("animal.species", string="Species", required=True)
    breed_id = fields.Many2one("animal.breed", string="Breed", required=True)
    color_id = fields.Many2one("animal.color", string="Color")
    size = fields.Char()
    weight = fields.Float(string="Weight (in kg)")
    birth_date = fields.Date()
    gender = fields.Selection(
        selection=[
            ("female", "Female"),
            ("male", "Male"),
            ("hermaphrodite", "Hermaphrodite"),
            ("neutered", "Neutered"),
        ],
        default="female",
        required=True,
    )
    active = fields.Boolean(default=True)
    image = fields.Binary(
        attachment=True, help="This field holds the photo of the animal."
    )

    @api.onchange("species_id")
    def onchange_species(self):
        self.breed_id = False

    @api.onchange("breed_id")
    def onchange_breed(self):
        self.color_id = False
