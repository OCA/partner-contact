# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 EXA Auto Parts S.A.S Guillermo Montoya <Github@guillermm>
# Copyright 2018 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# Copyright 2020 EXA Auto Parts S.A.S Juan Ocampo <Github@Capriatto>
# Copyright 2021 EXA Auto Parts S.A.S Alejandro Olano <Github@alejo-code>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons.partner_firstname import exceptions


class ResPartner(models.Model):
    """Adds other names."""
    _inherit = "res.partner"

    othernames = fields.Char("Other Names")

    @api.model
    def _get_computed_name(self, firstname, othernames, lastname, lastname2):
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
            if othernames:
                names.append(othernames)
            if lastname:
                names.append(lastname)
            if lastname2:
                names.append(lastname2)
        else:
            if lastname:
                names.append(lastname)
            if lastname2:
                names.append(lastname2)
            if names and (firstname or othernames) \
                    and order == 'last_first_comma':
                names[-1] = names[-1] + ","
            if firstname:
                names.append(firstname)
            if othernames:
                names.append(othernames)
        return u" ".join(names)

    @api.depends("firstname", "othernames", "lastname", "lastname2")
    def _compute_name(self):
        """Write the 'name' according to splitted data."""
        for partner in self:
            partner.name = self._get_computed_name(partner.firstname,
                                                   partner.othernames,
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
            record.othernames = parts['othernames']

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
            'othernames': False,
            'lastname': name or False,
            'lastname2': False,
        }

        if not is_company and name:
            order = self._get_names_order()
            result = super()._get_inverse_name(name, is_company)
            parts = []

            if order == 'first_last':
                if result['lastname2']:
                    parts = result['lastname2'].split(" ", 1)
                while len(parts) < 2:
                    result['othernames'] = False
                    return result
                result['othernames'] = result['lastname']
                result['lastname'] = parts[0]
                result['lastname2'] = parts[1]
            else:
                if result['firstname']:
                    parts = result['firstname'].split(" ", 1)
                while len(parts) < 2:
                    parts.append(False)
                result['firstname'] = parts[0]
                result['othernames'] = parts[1]

        return result

    @api.constrains("firstname", "othernames", "lastname", "lastname2")
    def _check_name(self):
        """Ensure at least one name is set."""
        try:
            super()._check_name()
        except exceptions.EmptyNamesError:
            for partner in self:
                if not partner.othernames:
                    raise

    @api.onchange("firstname", "othernames", "lastname", "lastname2")
    def _onchange_subnames(self):
        """Trigger onchange with 'othernames' too."""
        super()._onchange_subnames()
