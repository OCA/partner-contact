# See LICENSE file for full copyright and licensing details.

from odoo import api, models, _


class PortalWizardUser(models.TransientModel):
    _inherit = 'portal.wizard.user'

    @api.multi
    def get_error_messages(self):
        error_msg = super(PortalWizardUser, self).get_error_messages()
        if error_msg:
            error_msg[-1] = '%s\n%s' % (
                error_msg[-1],
                _("- Merge existing contacts together using the Automatic "
                  "Merge wizard, available in the Action menu after selecting "
                  "several contacts in the Customers list"))
        return error_msg
