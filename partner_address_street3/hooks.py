# -*- coding: utf-8 -*-
# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def street3_post_init_hook(cr, registry):
    query = """
        UPDATE res_country
        SET address_format = replace(
        address_format,
        E'\n%(street2)s',
        E'\n%(street2)s\n%(street3)s'
        )
    """
    cr.execute(query)


def street3_uninstall_hook(cr, registry):
    query = """
        UPDATE res_country
        SET address_format = replace(
        address_format,
        E'\n%(street3)s',
        ''
        )
    """
    cr.execute(query)
