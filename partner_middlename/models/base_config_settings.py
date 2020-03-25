# -*- coding: utf-8 -*-
# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 EXA Auto Parts S.A.S Guillermo Montoya <Github@guillermm>
# Copyright 2018 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    def _partner_names_order_selection(self):
        options = super(BaseConfigSettings,
                        self)._partner_names_order_selection()

        new_labels = {
            'last_first': 'Lastname SecondLastname Firstname middlename',
            'last_first_comma': 'Lastname SecondLastname,\
                Firstname middlename',
            'first_last': 'Firstname middlename Lastname SecondLastname'}

        return [(k, new_labels[k]) if k in
                new_labels else (k, v) for k, v in options]

    @api.multi
    def _partners_for_recalculating(self):
        res = super(BaseConfigSettings, self)._partners_for_recalculating()
        res |= self.env['res.partner'].search([
            ('is_company', '=', False),
            '|',
            '&',
            ('middlename', '!=', False),
            ('lastname', '!=', False),
            '&',
            ('middlename', '!=', False),
            ('lastname2', '!=', False)])
        return res
