# Copyright 2013 Nicolas Bessi (Camptocamp SA)
# Copyright 2014 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 Grupo ESOC (<http://www.grupoesoc.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = ["res.users", "firstname.mixin"]

    def copy(self, default=None):
        default_ = default or {}
        records = self.browse()
        for record in self:
            default = dict(default_)
            if ("name" not in default) and ("partner_id" not in default):
                default["name"] = self.env._("%(name)s (copy)", name=record.name)
            if "login" not in default:
                default["login"] = self.env._("%(login)s (copy)", login=record.login)
            if (
                ("firstname" not in default)
                and ("lastname" not in default)
                and ("name" in default)
            ):
                default.update(
                    self.env["res.partner"]._get_inverse_name(default["name"], False)
                )
            records |= super(ResUsers, record).copy(default)
        return records
