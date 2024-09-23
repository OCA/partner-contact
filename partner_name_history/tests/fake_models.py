#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FakeModel(models.Model):
    _name = "fake.model"
    _description = "Fake model used in tests"
    _partner_name_history_field_map = {
        "partner_id": "date",
    }

    partner_id = fields.Many2one(
        comodel_name="res.partner",
    )
    date = fields.Date()


class FakeModelMethod(models.Model):
    _name = "fake.model.method"
    _description = "Fake model with method used in tests"
    _partner_name_history_field_map = {
        "partner_id": "_get_name_history_date",
    }

    partner_id = fields.Many2one(
        comodel_name="res.partner",
    )
    date = fields.Date()

    def _get_name_history_date(self):
        self.ensure_one()
        return self.date


class FakeModelWrongMap(models.Model):
    _name = "fake.model.wrong_map"
    _description = "Fake model with method used in tests"
    _partner_name_history_field_map = {
        "partner_id": "datte",
    }

    partner_id = fields.Many2one(
        comodel_name="res.partner",
    )
    date = fields.Date()
