# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, exceptions, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sector_id = fields.Many2one(comodel_name='res.partner.sector',
                                string='Main Sector')

    secondary_sector_ids = fields.Many2many(
        comodel_name='res.partner.sector', string="Secondary Sectors",
        domain="[('id', '!=', sector_id)]")

    @api.constrains('sector_id', 'secondary_sector_ids')
    def _check_sectors(self):
        if self.sector_id in self.secondary_sector_ids:
            raise exceptions.UserError(_('The main sector must be different '
                                       'from the secondary sectors.'))
