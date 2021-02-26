# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 EXA Auto Parts S.A.S Guillermo Montoya <Github@guillermm>
# Copyright 2018 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# Copyright 2020 EXA Auto Parts S.A.S Juan Ocampo <Github@Capriatto>
# Copyright 2021 EXA Auto Parts S.A.S Alejandro Olano <Github@alejo-code>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _partner_names_order_selection(self):
        options = super()._partner_names_order_selection()

        new_labels = {
            'last_first':
            'Lastname SecondLastname \
                Firstname Othernames',
            'last_first_comma':
            'Lastname SecondLastname, \
                Firstname Othernames',
            'first_last':
            'Firstname Othernames \
                Lastname SecondLastname',
        }
        return [(k, new_labels[k]) if k in new_labels else (k, v)
                for k, v in options]

    @api.multi
    def _partners_for_recalculating(self):
        return self.env['res.partner'].search([
            ('is_company', '=', False), '|', '&', ('firstname', '!=', False),
            ('lastname', '!=', False), '|', '&', ('firstname', '!=', False),
            ('lastname2', '!=', False), '|', '&', ('othernames', '!=', False),
            ('lastname', '!=', False), '&', ('othernames', '!=', False),
            ('lastname2', '!=', False)
        ])
