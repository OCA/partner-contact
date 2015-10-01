# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de servicios, S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import string
from openerp import _, api, exceptions, fields, models
from openerp.addons.base_vat.base_vat import _ref_vat


class PartnerVATInContacts(models.Model):
    """Allow to set up individual VAT for a company's contacts."""
    _inherit = "res.partner"

    contact_vat = fields.Char(
        "Contact TIN",
        size=32,
        help="Tax Identification Number of the contact. "
             "This will not be used for commercial actions; "
             "instead, parent company's TIN will be used.")

    @api.multi
    @api.constrains("is_company", "contact_vat")
    def contact_vat_check(self):
        """Check validity of `contact_vat`.

        It does not use VIES because usually it would fail when checking
        persons' VAT codes.
        """
        for s in self.filtered(lambda r: not r.is_company and r.contact_vat):
            country, code = s._split_vat(s.contact_vat)
            values = {
                "vat": s.contact_vat,
                "name": s.display_name,
            }

            # VAT should start with 2 letters
            if any(char not in string.ascii_lowercase for char in country):
                raise exceptions.ValidationError(
                    _("VAT %(vat)s of %(name)s should start with "
                      "2 letters that indicate the country code.") % values)

            # Use core methods for VAT checking
            elif not s.simple_vat_check(country, code):
                # Display a useful message to user
                values["template"] = (
                    _ref_vat.get(country) or
                    _("CCNNNNNNNNN (CC=Country Code of 2 letters, "
                      "NNN... Local VAT number)."))
                raise exceptions.ValidationError(
                    _("VAT %(vat)s of %(name)s has a wrong format. "
                      "It should be similar to %(template)s") % values)
