# -*- coding: utf-8 -*-
# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 EXA Auto Parts S.A.S Guillermo Montoya <Github@guillermm>
# Copyright 2018 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons.partner_firstname import exceptions


class ResPartner(models.Model):
    """Adds other names."""
    _inherit = "res.partner"

    middlename = fields.Char("Other Names")

    @api.model
    def _get_computed_name(self, firstname, middlename, lastname, lastname2):
        """
        Compute the name combined with the other names too.

        We have 2 lastnames , so lastnames and the firstname
        and the other names will be separated by a comma.
        """
        order = self._get_names_order()
        names = list()

        if order == 'first_last':
            if firstname:
                names.append(firstname)
            if middlename:
                names.append(middlename)
            if lastname:
                names.append(lastname)
            if lastname2:
                names.append(lastname2)
        else:
            if lastname:
                names.append(lastname)
            if lastname2:
                names.append(lastname2)
            if names and (firstname or middlename) and \
                    order == 'last_first_comma':
                names[-1] = names[-1] + ","
            if firstname:
                names.append(firstname)
            if middlename:
                names.append(middlename)
        return u" ".join(names)

    @api.depends("firstname", "middlename", "lastname", "lastname2")
    def _compute_name(self):
        """Write the 'name' according to splitted data."""
        for partner in self:
            partner.name = self._get_computed_name(
                partner.firstname,
                partner.middlename,
                partner.lastname,
                partner.lastname2)

    @api.model
    def _names_order_default(self):
        return 'first_last'

    @api.multi
    def _inverse_name(self):
        """Try to revert the effect of '_compute_name'."""
        for record in self:
            parts = record._get_inverse_name(record.name, record.is_company)
            record.lastname = parts['lastname']
            record.lastname2 = parts['lastname2']
            record.firstname = parts['firstname']
            record.middlename = parts['middlename']

    @api.model
    def _get_inverse_name(self, name, is_company=False):
        """
        Compute the inverted name.
        - If the partner is a company, save it in the lastname.
        - Otherwise, make a guess.
        """
        # Company name goes to the lastname
        result = {
            'firstname': False,
            'middlename': False,
            'lastname': name or False,
            'lastname2': False,
        }

        if not is_company and name:
            order = self._get_names_order()
            result = super(ResPartner,
                        self)._get_inverse_name(name,is_company)
            parts = []

            if order == 'first_last':
                if result['lastname2']:
                    parts = result['lastname2'].split(" ", 1)
                while len(parts) < 2:
                    result['middlename'] = False
                    return result
                result['middlename'] = result['lastname']
                result['lastname'] = parts[0]
                result['lastname2'] = parts[1]
            else:
                if result['firstname']:
                    parts = result['firstname'].split(" ", 1)
                while len(parts) < 2:
                    parts.append(False)
                result['firstname'] = parts[0]
                result['middlename'] = parts[1]

        return result

    @api.constrains("firstname", "middlename", "lastname", "lastname2")
    def _check_name(self):
        """Ensure at least one name is set."""
        for partner in self:
            try:
                super(ResPartner, partner)._check_name()
            except exceptions.EmptyNamesError:
                if not partner.middlename:
                    raise

    @api.onchange("firstname", "middlename", "lastname", "lastname2")
    def _onchange_subnames(self):
        """Trigger onchange with 'middlename' too."""
        super(ResPartner, self)._onchange_subnames()
