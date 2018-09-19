# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade
from psycopg2.extensions import AsIs


def fill_res_partner_industry(cr):
    cr.execute(
        """
        INSERT INTO res_partner_industry (name, active, create_uid,
            create_date, write_uid, write_date, %s)
        SELECT name, TRUE as active, create_uid, create_date, write_uid,
            write_date, id
        FROM res_partner_sector
        """, (AsIs(openupgrade.get_legacy_name('old_sector_id')), ),
    )
    # corrected parent_id here:
    cr.execute(
        """
        UPDATE res_partner_industry rpi
        SET parent_id = rpi2.id
        FROM res_partner_sector rps
        INNER JOIN res_partner_industry rpi2 ON rps.parent_id = rpi2.%s
        WHERE rpi.%s = rps.id
        """, (
            AsIs(openupgrade.get_legacy_name('old_sector_id')),
            AsIs(openupgrade.get_legacy_name('old_sector_id')),
        ),
    )


def update_res_partner_industry(cr):
    cr.execute(
        """
        UPDATE res_partner rp
        SET industry_id = rpi.id
        FROM res_partner_industry rpi
        WHERE rp.%s IS NOT NULL AND rp.%s = rpi.%s
        """, (
            AsIs(openupgrade.get_legacy_name('sector_id')),
            AsIs(openupgrade.get_legacy_name('sector_id')),
            AsIs(openupgrade.get_legacy_name('old_sector_id')),
        ),
    )


def fill_res_partner_industry_secondary(cr):
    cr.execute(
        """
        INSERT INTO res_partner_res_partner_industry_rel (res_partner_id,
            res_partner_industry_id)
        SELECT rel.res_partner_id, rpi.id
        FROM res_partner_res_partner_sector_rel rel
        LEFT JOIN res_partner_industry rpi
            ON rel.res_partner_sector_id = rpi.%s
        """, (AsIs(openupgrade.get_legacy_name('old_sector_id')), ),
    )


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    cr = env.cr
    if openupgrade.table_exists(cr, 'res_partner_sector'):
        fill_res_partner_industry(cr)
        env['res.partner.industry']._parent_store_compute()
        update_res_partner_industry(cr)
        fill_res_partner_industry_secondary(cr)
