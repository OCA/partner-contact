# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from psycopg2.extensions import AsIs
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    column_name = openupgrade.get_legacy_name('better_zip_id')
    openupgrade.logged_query(
        env.cr,
        "ALTER TABLE res_city_zip ADD %s INTEGER", (AsIs(column_name), ),
    )
    # Create a city for ZIPs without it
    openupgrade.logged_query(
        env.cr, """
        INSERT INTO res_city (
            name, state_id, country_id,
            create_uid, create_date, write_uid, write_date
        )
        SELECT
            city, state_id, country_id,
            MIN(create_uid), MIN(create_date), MIN(write_uid), MIN(write_date)
        FROM res_better_zip
        WHERE city_id IS NULL
        GROUP BY city, state_id, country_id
        ON CONFLICT DO NOTHING""",
    )
    # Update city_id in res_better_zip
    openupgrade.logged_query(
        env.cr, """
        UPDATE res_better_zip rbz
        SET city_id = rc.id
        FROM res_city rc
        WHERE rc.name = rbz.city
            AND rc.state_id = rbz.state_id
            AND rc.country_id = rbz.country_id
            AND rbz.city_id IS NULL""",
    )
    # Create records for new model
    openupgrade.logged_query(
        env.cr, """
        INSERT INTO res_city_zip (
            %s, name, city_id
        )
        SELECT
            id, name, city_id
        FROM res_better_zip
        WHERE city_id IS NOT NULL
        ON CONFLICT DO NOTHING""",
        (AsIs(column_name), ),
    )
    # Recompute display name for entries inserted by SQL
    env['res.city.zip'].search([])._compute_new_display_name()
    # Link res.partner with corresponding new entries
    openupgrade.logged_query(
        env.cr, """
        UPDATE res_partner rp
        SET zip_id = rcz.id
        FROM res_city_zip rcz
        WHERE rcz.%s = rp.%s""",
        (AsIs(column_name), AsIs(openupgrade.get_legacy_name('zip_id')), ),
    )
