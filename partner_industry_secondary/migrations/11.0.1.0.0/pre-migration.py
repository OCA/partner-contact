# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

_xmlid_renames = [
    ('partner_industry_secondary.group_use_partner_sector_for_person',
     'partner_industry_secondary.group_use_partner_industry_for_person'),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, _xmlid_renames)
    # No need to check existence, as if getting to this, it will exist
    openupgrade.rename_tables(
        env.cr, [('res_partner_res_partner_sector_rel',
                  'res_partner_res_partner_industry_rel')],
    )
    openupgrade.rename_columns(env.cr, {
        'res_partner_res_partner_industry_rel': [
            ('res_partner_sector_id', 'res_partner_industry_id'),
        ]
    })
