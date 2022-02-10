# Copyright 2022 Riverminds Cia Ltda - Mamfredy Mejia Matute
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models


class ResParish(models.Model):
    _name = "res.parish"
    _order = "name"

    name = fields.Char("Name", required=True, translate=True)
    code = fields.Char("Code")
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one(
        'res.country.state', 'State', domain="[('country_id', '=', country_id)]")
    city_id = fields.Many2one(
        'res.city', 'City', domain="[('state_id', '=', state_id)]")

    def name_get(self):
        res = []
        for parish in self:
            name = parish.name if not parish.code else '%s (%s)' % (parish.name, parish.code)
            res.append((parish.id, name))
        return res

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        # optimize out the default criterion of ``ilike ''`` that matches everything
        if not (name == '' and operator == 'ilike'):
            args += ['|', (self._rec_name, operator, name), ('code', operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)