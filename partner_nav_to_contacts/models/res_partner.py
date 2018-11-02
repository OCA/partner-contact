# SDI
# © 2018 David Juaneda <djuaneda@sdi.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    contact_origin = fields.Many2one('res.partner', string='Contact origin')

    @api.multi
    def open_commercial_partner(self):
        """
        It redirects us to the contact form view.
        """
        self.ensure_one()
        return {'type': 'ir.actions.act_window',
                'res_model': 'res.partner',
                'view_mode': 'form',
                'res_id': self.id,
                'target': 'current',
                'flags': {'form': {'action_buttons': False}}}
