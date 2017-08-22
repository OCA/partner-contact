# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):

    cr.execute(
        'UPDATE res_partner SET partner_company_type_id = company_type_id'
    )
