# -*- coding: utf-8 -*-
# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 Guillermo Montoya <Github@guillermm>
# Copyright 2018 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.onchange("firstname", "othernames", "lastname", "lastname2")
    def _compute_name(self):
        """Write the 'name' field according to splitted data."""
        for partner in self:
            partner.name = partner.partner_id._get_computed_name(
                partner.firstname,
                partner.othernames,
                partner.lastname,
                partner.lastname2)
