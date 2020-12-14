# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 EXA Auto Parts S.A.S Guillermo Montoya <Github@guillermm>
# Copyright 2018 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# Copyright 2018 EXA Auto Parts S.A.S Juan Ocampo <Github@Capriatto>
# Copyright 2020 EXA Auto Parts S.A.S Alejandro Olano <Github@alejo-code>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, exceptions


class EmptyNamesError(exceptions.ValidationError):
    def __init__(self, record, value=_("No name is set.")):
        self.record = record
        self._value = value
        self.name = _("Error(s) with partner %d's name.") % record.id
        self.args = (self.name, value)
