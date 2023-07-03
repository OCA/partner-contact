# © 2014-2015 Tecnativa S.L. - Jairo Llopis
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    department_id = fields.Many2one("res.partner.department", "Department")
