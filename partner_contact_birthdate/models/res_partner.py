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
    age = fields.Integer(
        string="Age", readonly=True, compute="_compute_age", search="_search_age"
    )

    @api.depends("birthdate_date")
    def _compute_age(self):
        for record in self:
            age = 0
            if record.birthdate_date:
                age = relativedelta(fields.Date.today(), record.birthdate_date).years
            record.age = age

    def _search_age(self, operator, value):
        if operator not in ("=", "!=", "<", "<=", ">", ">="):
            return []
        # pylint: disable=sql-injection
        # the value of operator is checked, no risk of injection
        query = """
            SELECT id
            FROM res_partner
            WHERE extract(year from age(CURRENT_DATE, birthdate_date))
              {operator} %s
            """.format(
            operator=operator
        )
        self.env.cr.execute(query, (value,))
        ids = [t[0] for t in self.env.cr.fetchall()]
        return [("id", "in", ids)]
