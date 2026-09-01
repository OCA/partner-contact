# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends("animal_ids")
    def _compute_animal_count(self):
        for rec in self:
            rec.animal_count = len(rec.animal_ids)

    animal_ids = fields.One2many("animal", "partner_id", string="Animals")
    animal_count = fields.Integer(
        compute=_compute_animal_count, string="Number of Animals", store=True
    )

    def action_view_animals(self):
        xmlid = "animal.action_animal"
        action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
        if self.animal_count > 1:
            action["domain"] = [("id", "in", self.animal_ids.ids)]
        else:
            action["views"] = [(self.env.ref("animal.view_animal_form").id, "form")]
            action["res_id"] = self.animal_ids and self.animal_ids.ids[0] or False
        return action
