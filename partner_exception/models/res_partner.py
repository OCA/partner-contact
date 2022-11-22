# Copyright 2022 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ExceptionRule(models.Model):
    _inherit = "exception.rule"

    model = fields.Selection(selection_add=[("res.partner", "Contact")])
    partner_ids = fields.Many2many("res.partner", string="Contacts")


class ResPartner(models.Model):
    _inherit = ["res.partner", "base.exception"]
    _name = "res.partner"
    _order = "main_exception_id asc, name desc"

    @api.model
    def _reverse_field(self):
        return "partner_ids"

    def _fields_trigger_check_exception(self):
        return ["ignore_exception"]

    @api.model
    def create(self, vals):
        record = super(ResPartner, self).create(vals)
        check_exceptions = any(
            field in vals for field in self._fields_trigger_check_exception()
        )
        if check_exceptions:
            record.contact_check_exception()
        return record

    def write(self, vals):
        result = super(ResPartner, self).write(vals)
        check_exceptions = any(
            field in vals for field in self._fields_trigger_check_exception()
        )
        if check_exceptions:
            self.contact_check_exception()
        return result

    def contact_check_exception(self):
        if self:
            self._check_exception()
