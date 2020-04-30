# Copyright (C) 2014-2015  Grupo ESOC <www.grupoesoc.es>
# Copyright 2017-Apertoso N.V. (<http://www.apertoso.be>)
# Copyright 2019-2020: Druidoo (<https://www.druidoo.io>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ResPartner(models.Model):
    """Partner with birth date in date format."""

    _inherit = "res.partner"

    birthdate_date = fields.Date("Birthdate")
    age = fields.Integer(string="Age", readonly=True, compute="_compute_age")

    @api.depends("birthdate_date")
    def _compute_age(self):
        for record in self:
            age = 0
            if record.birthdate_date:
                age = relativedelta(fields.Date.today(), record.birthdate_date).years
            record.age = age
