# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.returns('self', lambda value: value.id)
    def message_post(self, *args, **kwargs):
        """Change user who is posting the message if set by context."""
        if self.env.context.get('message_post_user'):
            obj = self.sudo(self.env.context['message_post_user'])
        else:
            obj = self
        return super(ResPartner, obj).message_post(*args, **kwargs)
