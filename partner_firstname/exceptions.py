# -*- coding: utf-8 -*-
# © 2014-2015 Grupo ESOC (<http://www.grupoesoc.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import _, exceptions


class EmptyNamesError(exceptions.ValidationError):
    def __init__(self, record, value=_("No name is set.")):
        self.record = record
        self._value = value
        self.name = _(
            "Error(s): at least one name (name, firstname or "
            "lastname)  is mandatory for partner (id : %d).") % record.id
        self.args = (self.name, value)
