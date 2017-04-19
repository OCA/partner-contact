# -*- coding: utf-8 -*-
# Copyright 2016 Acsone S.A.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from stdnum import ean
from stdnum.exceptions import InvalidChecksum
from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gln = fields.Char(size=13, string='GLN',
                      help='This is the company GLN identification number.')

    @api.multi
    @api.constrains('gln')
    def _check_gln(self):

        for partner in self:
            if partner.gln:
                try:
                    ean.validate(partner.gln)
                except InvalidChecksum, e:
                        raise ValidationError(_('The GLN field for the partner'
                                                ' %s is not valid! %s')
                                              % (partner.name, e.message))

    @api.multi
    @api.constrains('gln')
    def _check_unique_gln(self):

        for partner in self:
            if partner.gln:
                duplicate_partners = self.search([('gln', '!=', False),
                                                  ('gln', '=', partner.gln),
                                                  ('id', '!=', partner.id)])

                if duplicate_partners:
                    raise ValidationError(_('GLN code is already used by '
                                            'existing partners : %s')
                                          % ','.join([p.name for p in
                                                      duplicate_partners]))
