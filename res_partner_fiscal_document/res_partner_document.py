# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) Odoo Colombia (Community).
# Author        David Arnold (devCO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _

class ResPartnerIDtype(models.Model):
    _name = 'res.partner.idtype'
    _description = 'Identification Document Type'
    _order = 'sequence'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    sequence = fields.Integer()
    active = fields.Boolean(default=True)
    note = fields.Text()
    on_company = fields.Boolean(string=u'On Company?')
    on_contact = fields.Boolean(string=u'On Contact?', default=True)


class ResPartnerIdent(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    dom = "['|', ('on_company', '=', is_company), ('on_contact', '!=', is_company)]"
    fiscal_id_type = fields.Many2one(
        'res.partner.idtype', string=u'Document Type', domain=dom,
    )
    fiscal_id = fields.Char(string=u'Document ID')
    fiscal_id_doc = fields.Binary(string=u'Document Scan',
                                  help="Upload the supporting Document preferably as size-optimized PDF. This might "
                                       "help save disk space and PDF allows you to concatenate multiple documents.")


    @api.one
    @api.onchange(
        'fiscal_id_type',
        'fiscal_id',
        # 'is_company', # https://github.com/odoo/odoo/issues/1530
    )
    def validateformatcopy(self):
        # CASE: Current ID Type is not applicable on company
        if self.is_company and not self.fiscal_id_type.on_company:
            # Get the first valid ID type (remember: ordered by sequence)
            self.fiscal_id_type = self.env['res.partner.idtype'].search([('on_company', '=', True)], limit=1).id
            self.fiscal_id = None # Reset ID value
        # CASE: Current ID Type is not applicable on contact
        if not self.is_company and not self.fiscal_id_type.on_contact:
            # Get the first valid ID type (remember: ordered by sequence)
            self.fiscal_id_type = self.env['res.partner.idtype'].search([('on_contact', '=', True)], limit=1).id
            self.fiscal_id = None # Reset ID value
        # If everything is fine, call subclasses
        if self.fiscal_id_type and self.fiscal_id:
            # Function for String Operations
            res = self._validateandformatid(self)
            if res['output_type'] and res['output_id']:
                self.fiscal_id_type, self.fiscal_id = res['output_type'], res['output_id']
            # Procedure for Copying
            self._copyid(self)


    @staticmethod
    def _validateandformatid(self):
        """
        Hook method to be inherited for custom validation methods.
        :param input_type: the value of the field fiscal_id_type (id); passed on by onchange decorator
        :param input_id: the value of the field fiscal_id (string); passed on by onchange decorator
        :return: must return a dict with validated and formatted values

        Hint:
        you might not alter the output_type unless you might want to build some kind of fiscal_id_type recognition
        based on the input pattern into your hook method. CO###.###.###-# CO-VAT (NIT) for example.

        Find below a suggested basic outline.

        """
        f_type, f_id, is_company = self.fiscal_id_type, self.fiscal_id, self.is_company

        def default(): return {'output_type': f_type, 'output_id': f_id}
        return {
            'CODE1': {'output_type': f_type, 'output_id': f_id},
            'CODE2': {'output_type': f_type, 'output_id': f_id},
            # Define your cases with the index being the doctype id to match
            # Note you can work inline (lambda), or call subfunctions at will
        }.get(self.fiscal_id_type.code,default())

    @staticmethod
    def _copyid(self):
        """
        Hook Method to be inherited for custom copy methods based on the document type (id)
        Example Use Case: Copy some local VAT number into the VAT-Field in it's international format for compatibility.

        :return: It is a Procedure and therefore has no return value.

        Find below a suggested basic outline.

        """
        f_type, f_id, is_company = self.fiscal_id_type, self.fiscal_id, self.is_company

        def stringop_def(s): return s
        def stringop_1(s): return re.match('\\d|\\w*', s)
        # Define other Docstringoperatios if necessary

        def default():
            self.vat_subjected = True
            # self.vat is a Boolean until base_vat is installed.
            # self.vat = self.country_id.code + sringop_def(f_id)

        {
            'CODE1': {# self.vat_subjected: True,
                # self.vat: self.country_id.code + stringop_1(f_id)
            },
            'CODE2': {# seld.vat_subjected: True,
                # self.vat: self.country_id.code + stringop_1(f_id)
            },
            }.get(self.fiscal_id_type.code, default())
