# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResCountry(models.Model):
    """Add labels corresponding to each country.

    These stay empty in this base module, and should be filled by l10n ones.
    """
    _inherit = "res.country"

    state_label = fields.Char(
        translate=True,
        help="Label for the state NUTS category.")
    substate_label = fields.Char(
        translate=True,
        help="Label for the substate NUTS category.")
    region_label = fields.Char(
        translate=True,
        help="Label for the region NUTS category.")
    state_level = fields.Integer(
        help="Level for the state NUTS category.")
    substate_level = fields.Integer(
        help="Level for the substate NUTS category.")
    region_level = fields.Integer(
        help="Level for the region NUTS category.")
