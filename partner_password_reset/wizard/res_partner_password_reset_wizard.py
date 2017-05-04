# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, exceptions, fields, models


class ResPartnerPasswordResetWizard(models.TransientModel):
    _name = 'res.partner.password.reset.wizard'

    user_ids = fields.Many2many(
        comodel_name='res.users',
        default=lambda s: s._default_user_ids(),
        required=True,
        readonly=True,
    )

    @api.multi
    def _default_user_ids(self):
        """ Return a RecordSet of `res.users` associated to the active IDs """
        partner_ids = self.env['res.partner'].browse(
            self.env.context.get('active_ids')
        )
        return partner_ids.mapped('user_ids')

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        """ Override to check that there are associated users when called """
        res = super(ResPartnerPasswordResetWizard, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=False)
        if not self._default_user_ids():
            raise exceptions.Warning(
                _('The selected partners have no associated portal users')
            )
        return res

    @api.multi
    def action_submit(self):
        """ Reset the user passwords on submission """
        self.mapped('user_ids').action_reset_password()
