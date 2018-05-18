# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from . import models
from odoo import api, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)

try:
    from openupgradelib import openupgrade
except (ImportError, IOError) as err:
    _logger.debug(err)


def not_demo_db(cr):
    """Check demo DB or not"""
    cr.execute("""SELECT id
      FROM public.ir_module_module
      WHERE demo = 'f'
      LIMIT 1""")
    module_record = cr.fetchone()
    if module_record[0]:
        return False
    return True


def get_create_res_partner_id_category(env, old_category_id):
    # license_type migration
    cr = env.cr
    query = """
        SELECT id, name
        FROM license_type
        WHERE id = %i""" % (old_category_id)
    cr.execute(query)
    record = cr.fetchone()
    rec_id, name = record
    res_id = env['res.partner.id_category'].search([
        ('name', '=', name)
    ])
    if not res_id:
        res_id = env['res.partner.id_category'].create({
            'code': name[:15],
            'name': name,
        })
    return res_id


def create_res_partner_id_number(
        env,
        partner_id,
        license_date,
        about2expired,
        category_id):
    env['res.partner.id_number'].create({
        'partner_id': partner_id,
        'category_id': category_id,
        'valid_until': license_date,
        'status': ('pending' if about2expired == 't' else 'open'),
    })


def migrate_partner_licence_information(env):
    # partner_license migration
    cr = env.cr
    query = """
        SELECT id, partner_id, about2expired, license_date, name
        FROM partner_license"""
    cr.execute(query)
    records = cr.fetchall()
    for record in records:
        rec_id, partner_id, about2expired, license_date, name = record
        res_partner_id_category_id = get_create_res_partner_id_category(name)
        create_res_partner_id_number(
            env,
            partner_id,
            license_date,
            about2expired,
            res_partner_id_category_id)


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    if not_demo_db(cr):
        if openupgrade.table_exists(env.cr, 'partner_license') and (
                openupgrade.table_exists(env.cr, 'licence_type')):
                    migrate_partner_licence_information(env)
