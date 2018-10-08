# Copyright 2016 Nicolas Bessi, Camptocamp SA
# Copyright 2018 Aitor Bouzas <aitor.bouzas@adaptivecity.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResCityZip(models.Model):
    """City/locations completion object"""

    _name = "res.city.zip"
    _description = __doc__
    _order = "name asc"
    _rec_name = "display_name"

    name = fields.Char('ZIP', required=True)
    city_id = fields.Many2one(
        'res.city',
        'City',
        required=True,
    )
    display_name = fields.Char(compute='_compute_new_display_name',
                               store=True, index=True)

    _sql_constraints = [
        ('name_city_uniq', 'UNIQUE(name, city_id)',
         'You already have a zip with that code in the same city. '
         'The zip code must be unique within it\'s city'),
    ]

    @api.multi
    @api.depends('name', 'city_id')
    def _compute_new_display_name(self):
        for rec in self:
            name = [rec.name, rec.city_id.name]
            if rec.city_id.state_id:
                name.append(rec.city_id.state_id.name)
            if rec.city_id.country_id:
                name.append(rec.city_id.country_id.name)
            rec.display_name = ", ".join(name)
