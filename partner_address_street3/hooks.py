# -*- coding: utf-8 -*-
# Copyright 2014 Nicolas Bessi, Alexandre Fayolle, Camptocamp SA
# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def post_init_hook(cr, registry):
    """ Add street3 to address format """
    query = """
        UPDATE res_country
        SET address_format = replace(
        address_format,
        E'%(street2)s\n',
        E'%(street2)s\n%(street3)s\n'
        )
    """
    cr.execute(query)


def uninstall_hook(cr, registry):
    """ Remove street3 from address format """
    # Remove %(street3)s\n format
    query = """
        UPDATE res_country
        SET address_format = replace(
        address_format,
        E'%(street3)s\n',
        ''
        )
    """
    cr.execute(query)
