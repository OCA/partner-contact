# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class EntityLegalFormAbbreviation(models.Model):
    _name = "entity.legal.form.abbreviation"
    _description = "Entity Legal Form Abbreviation Model"

    name = fields.Char()
    entity_legal_form_id = fields.Many2one(
        "entity.legal.form", string="Entity Legal Form"
    )

    _sql_constraints = [
        (
            "name_uniq",
            "unique (name, entity_legal_form_id)",
            "Abbreviation already exists!",
        )
    ]
