# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade
from psycopg2.extensions import AsIs

_column_renames = {
    'res_partner': [('sector_id', None)],
}

_xmlid_renames = [
    ('partner_sector.group_use_partner_sector_for_person',
     'partner_industry_secondary.group_use_partner_industry_for_person'),
]


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    cr = env.cr
    if openupgrade.table_exists(cr, 'res_partner_sector'):
        openupgrade.rename_columns(cr, _column_renames)
        openupgrade.rename_xmlids(cr, _xmlid_renames)
        cr.execute(
            """
            ALTER TABLE res_partner_industry
            ADD COLUMN %s integer;
            """, (AsIs(openupgrade.get_legacy_name('old_sector_id')), ),
        )
