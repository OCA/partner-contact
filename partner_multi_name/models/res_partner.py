# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 EXA Auto Parts S.A.S Guillermo Montoya <Github@guillermm>
# Copyright 2018 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# Copyright 2020 EXA Auto Parts S.A.S Juan Ocampo <Github@Capriatto>
# Copyright 2021 EXA Auto Parts S.A.S Alejandro Olano <Github@alejo-code>
# Copyright 2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    """Adds other names."""

    _inherit = "res.partner"

    othernames = fields.Char("Other Names")

    def _get_firstname_fields(self):
        """Determine dynamically the fields that compose the first name."""
        return super()._get_firstname_fields() + ["othernames"]

    def _inverse_name(self):
        """Try to revert the effect of '_compute_name'."""
        for record in self:
            parts = record._get_inverse_name(record.name, record.is_company)
            record.lastname = parts["lastname"]
            record.lastname2 = parts["lastname2"]
            record.firstname = parts["firstname"]
            record.othernames = parts["othernames"]

    @api.model
    def _get_inverse_name(self, name, is_company=False):
        """
        Compute the inverted name.
        - If the partner is a company, save it in the lastname.
        - Otherwise, make a guess.
        """
        # Company name goes to the lastname
        result = {
            "firstname": False,
            "othernames": False,
            "lastname": name or False,
            "lastname2": False,
        }
        if not is_company and name:
            order = self._get_names_order()
            result = super()._get_inverse_name(name, is_company)
            parts = []
            if order == "first_last":
                if result["lastname2"]:
                    parts = result["lastname2"].split(" ", 1)
                while len(parts) < 2:
                    result["othernames"] = False
                    return result
                result["othernames"] = result["lastname"]
                result["lastname"] = parts[0]
                result["lastname2"] = parts[1]
            else:
                if result["firstname"]:
                    parts = result["firstname"].split(" ", 1)
                while len(parts) < 2:
                    parts.append(False)
                result["firstname"] = parts[0]
                result["othernames"] = parts[1]
        return result
