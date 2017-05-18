# -*- coding: utf-8 -*-
# © 2017 Sunflower IT <http://sunflowerweb.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def deduplicate_on_field(self, field, domain=[]):
        """ Merge contacts"""
        self.merge_wizard = \
            self.env['base.partner.merge.automatic.wizard']
        wizard_id = self.merge_wizard.with_context(
            extra_domain=domain).create({
                'group_by_%s' % (field,): True,
                'state': 'option'
            })
        wizard_id.automatic_process_cb()
