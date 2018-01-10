# © 2018 Apruzzese Francesco <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    fax = fields.Char()
