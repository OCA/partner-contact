# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=missing-docstring,protected-access
from openerp.osv import orm, fields


class ResPartner(orm.Model):
    _inherit = 'res.partner'

    _columns = {
        'coc_registration_number': fields.function(
            lambda self, *args, **kwargs:
            self._compute_identification(*args, **kwargs),
            arg='coc',
            fnct_inv=lambda self, *args, **kwargs:
            self._inverse_identification(*args, **kwargs),
            fnct_inv_arg='coc',
            type='char',
            fnct_search=lambda self, *args, **kwargs:
            self._search_identification(*args, **kwargs),
            method=True, readonly=False,
            string='CoC Registration Number',
        ),
    }
