# -*- coding: utf-8 -*-
# © 2017 Sunflower IT <http://sunflowerweb.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class ResPartnerChanges(models.Model):
    _inherit = 'res.partner'

    @api.model
    def deduplicate_on_fields(self, fields_list, domain=None):
        """ Merge contacts """
        wizard_obj = self.env['base.partner.merge.automatic.wizard']
        if domain:
            wizard_obj = wizard_obj.with_context(partner_merge_domain=domain)
        params = {'state': 'option'}
        for field in fields_list:
            params['group_by_%s' % (field,)] = True
        wizard = wizard_obj.create(params)
        wizard.automatic_process_cb()
