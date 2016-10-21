# -*- coding: utf-8 -*-
# © 2016 Akretion - Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, SUPERUSER_ID


def update_street3_on_countries(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        for country in env['res.country'].search([]):
            old = country.address_format
            if (
                    old and
                    '%(street2)s' in old and
                    '%(street3)s' not in old):
                index = old.find('%(street2)s') + len('%(street2)s')
                new = old[:index] + '\n%(street3)s' + old[index:]
                country.address_format = new
    return
